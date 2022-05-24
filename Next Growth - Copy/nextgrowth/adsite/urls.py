from . import views
from django.urls import path


urlpatterns = [
    path('', views.submit),
    path('submit', views.home),
    path('login', views.login),
    path('register', views.register),
]