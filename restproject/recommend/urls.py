from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view()),
    path('login/', views.Login.as_view()),
    path('home/', views.MainUrl().as_view()),
    path('temp/', views.Temp().as_view()),
]