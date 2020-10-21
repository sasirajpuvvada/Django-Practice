from django.contrib import admin
from django.urls import path

from .views import ArticleView

urlpatterns = [
    path('articles/', ArticleView.as_view()),
    path('articles/<int:pk>', ArticleView.as_view()),
]
