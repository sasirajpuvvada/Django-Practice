from django.contrib import admin
from django.urls import path
from calculate import views

urlpatterns = [
    path('', views.index,name='calculate'),
]