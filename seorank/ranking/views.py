from django.db.models import F
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .forms import SearchForm, LoginForm, UserForm, UserProfileInfoForm
from .models import Domain, Keyword, KeywordRankHistory

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from django.views import generic

import requests as req

# self-made function
# SEO rank function
def seorank(query, targetLink):
    API_KEY = ""
    SEARCH_ENGINE_ID = "e0e72fcc9580b4cb7"
    C2COFF = 0
    SAFE = "active"
    HL = "zh-TW"
    LR = "lang_zh-TW"
    page, i = 1, 0
    while page <= 10:
        start = (page - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&hl={HL}&lr={LR}&c2coff={C2COFF}&safe={SAFE}&q={query}&start={start}"
        data = req.get(url).json()
        search_items = data.get("items")
        if search_items == None:
            print("Error: There is no search_items.")
            return "請檢查域名輸入是否正確，若確定沒問題請找管理員。"
        else:
            for search_item in search_items:
                i+=1
                if targetLink in search_item.get("link"):
                    return i
            page+=1
    return "Above 100"

# Create your views here.
def index(request):

    return render(request, 'ranking/index.html')

def search_rank(request):
    combine_list = []
    if request.user.is_authenticated:
        if request.method=='POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                # print(data)
                form = SearchForm()
                keyword_list = data['keyword'].split(',')
                # print(keyword_list)
                rank_list = [0 for i in keyword_list]
                # print(rank_list)
                for i, keyword in enumerate(keyword_list):
                    # print(i, keyword, type(keyword))
                    rank_list[i] = seorank(keyword, data['domain_name'])
                
                try:
                    new_domain, created = Domain.objects.get_or_create(
                        user = request.user,
                        domain_name = data['domain_name']
                    )
                    print("Domain GET/CREATE")
                    if not created:
                        new_domain.save()
                        print("Domain ADD")
                except:
                    print(f"Domain: Not sure what will happen here")
                    # print(f"Already have this {data["domain_name"]} in Doamin database")

                combine_list = zip(keyword_list, rank_list)
                print(combine_list)

                for keyword, rank_value in combine_list:
                    try:
                        keyword_obj, created = Keyword.objects.get_or_create(
                            domain_name = new_domain,
                            keyword_name = keyword
                        )
                        print("Keyword GET/CREATE")
                        if not created:
                            keyword_obj.save()
                            print("Keyword ADD")
                    except:
                        print(f"Keyword: Not sure what will happen here")
                        # print("Already have this keyword in Keyword database")

                    new_rank_history = KeywordRankHistory(
                        keyword_name = keyword_obj,
                        rank = rank_value
                    )
                    new_rank_history.save()
                    print(f"Rank is saved.")
                    print(f"{keyword}:{rank_value}")
        else:
            form = SearchForm()
            data = {'domain_name':''}
            keyword_list = []
            rank_list = []

        combine_list = zip(keyword_list, rank_list)
        return render(request, 'ranking/seosearch.html',
                    context = {'form':form,
                                'domain_name':data['domain_name'],
                                'combine_list':combine_list},)
    else:
        return HttpResponseRedirect("login")

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('ranking:index'))
    else:
        if request.method=='POST':
            form = LoginForm
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('ranking:index'))
                else:
                    return HttpResponse("ACCOUNT NOT ACTIVE")
            else:
                print("Someone tried to login and failed!")
                print("Username: {} and password {}".format(username, password))
            
            return HttpResponse("Invalid login details supplied!")
        else:
            form = LoginForm
            return render(request, 'ranking/login.html',
                        context = {'form':form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ranking:index'))

def signup(request):
    logined = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return render(request, 'ranking/index.html')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm
        profile_form = UserProfileInfoForm

    return render(request, 'ranking/signup.html',
                  context = {'user_form':user_form,
                             'profile_form':profile_form,
                             'logined':logined})

def search_history(request):
    if request.user.is_authenticated:
        domain_obj = Domain.objects.filter(user=request.user)
        for obj in domain_obj:
            print(obj.domain_name)
        return render(request, 'ranking/search_history.html',
                      context={'search_history':domain_obj})
    else:
        return HttpResponseRedirect("login")

def single_history(request, domain_name):
    domain_obj = Domain.objects.filter(user=request.user, domain_name=domain_name).prefetch_related("keywords")
    keywords_list = []
    for D_obj in domain_obj:
        keyword_obj = D_obj.keywords.all()
        for K_obj in keyword_obj:
            keywords_list.append(K_obj.keyword_name)
    print(keywords_list)
    return render(request, 'ranking/single_history.html',
                  context={"keywords_list":keywords_list,
                           "domain_name":domain_name})

def rank_history(request, domain_name, keyword_name):
    print(f"Domain name: {domain_name}")
    print(f"Keyword name: {keyword_name}")
    domain_obj = Domain.objects.filter(user=request.user, domain_name=domain_name).prefetch_related("keywords__rank_history")
    rank_list = []
    for D_obj in domain_obj:
        for K_obj in D_obj.keywords.filter(keyword_name=keyword_name):
            for R_obj in K_obj.rank_history.order_by("-created_at"):
                rank_list.append(R_obj.rank)
    print(rank_list)
    return render(request, 'ranking/rank_history.html',
                context={"rank_list":rank_list,
                        "keyword_name":keyword_name,
                        "domain_name":domain_name})