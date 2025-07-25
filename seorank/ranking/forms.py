from django import forms
from django.contrib.auth.models import User
from django.db import models
from ranking.models import UserProfileInfo

# Form for search SEO RANK
class SearchForm(forms.Form):
    domain_name = forms.CharField(label="域名", max_length=200, widget=forms.TextInput(attrs={"placeholder":"xxx.com"}))
    keyword = forms.CharField(label="關鍵字", max_length=200, widget=forms.TextInput(attrs={"placeholder":"關鍵字1,關鍵字2,關鍵字3"}))

# Form for LOGIN
class LoginForm(forms.Form):
    username = forms.CharField(label="使用者名稱", max_length=200, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"使用者名稱"}))
    password = forms.CharField(label="密碼", max_length=128, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"密碼"}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"密碼",
        "required":True
        }))

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)
        widgets = {
            'username':forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"使用者名稱",
                "required":True
                }),
            'last_name':forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"姓氏",
                "required":True
                }),
            'first_name':forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"名字",
                "required":True
                }),
            'email':forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"你的信箱@mail.com",
                "required":True
                }),
        }

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('nickname',)
        widgets = {
            'nickname':forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"暱稱",
                "required":True
            })
        }