from django.urls import path
from . import views

app_name = 'ranking'

urlpatterns = [
    path("", views.index, name="index"),
    path("seosearch", views.search_rank, name="seosearch"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("search_history", views.search_history, name="search_history"),
    path("single_history/<str:domain_name>", views.single_history, name="single_history"),
    path("rank_history/<str:domain_name>/<str:keyword_name>", views.rank_history, name="rank_history"),
]