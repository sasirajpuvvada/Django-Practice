from django.contrib import admin
from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_list,name='contact'),
    path('<int:contact_id>/', views.detail, name='detail'),
    path('<int:contact_id>/delete/', views.delete, name='delete'),
    path('create/', views.contact_create_view,name = 'create'),
    path('<int:contact_id>/edit/', views.contact_edit,name = 'edit'),
]