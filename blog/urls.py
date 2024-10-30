# blog/urls.py
# description: app specific URLS for blog application

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(r'', views.RandomArticleView.as_view(), name="random"),
    path(r'show_all', views.ShowAllView.as_view(), name="show_all"),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"),
    path(r'create_article', views.CreateArticleView.as_view(), name="create_article"),
    # creating an authentication/sign on system for only the blog application
    path(r'login/', auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page="show_all"), name="logout"),
]