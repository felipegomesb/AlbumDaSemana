from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('users/<str:username>/', views.get_user_by_username, name='get_user_by_username'),
    path('users/<str:pk>/', views.get_user_by_pk, name='get_user_by_pk'),
    path('data/', views.user_manager, name='user_manager'),
]

