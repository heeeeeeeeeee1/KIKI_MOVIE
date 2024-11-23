# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:user_pk>/', views.profile),
]
