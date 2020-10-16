from django.contrib import admin
from django.urls import path
from webscrap import views

urlpatterns = [
    path('', views.index,name='webscrap'),
]