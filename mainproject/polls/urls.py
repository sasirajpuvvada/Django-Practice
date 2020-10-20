from django.contrib import admin
from django.urls import path, include
from . import views
from django.http import Http404
from django.shortcuts import render

app_name = 'polls'
urlpatterns = [
    path('', views.index,name = 'index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]