from . import views
from django.urls import path, re_path, include
from . import views
from rest_framework import routers



urlpatterns = [
    path('home', views.home),
    path('login', views.login),
    path('api', views.apifetch),
    path('register', views.register),
    re_path(r'^appdetail/(?P<task>\w{0,50})$', views.appdetails),
    re_path('appdetail/upload/', views.appdetails),
    path('profile', views.profile),
    path('points', views.points),
    path('tasks', views.tasks),
    path('logout', views.logout),
]