# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('profile/<int:user_pk>/', views.profile),
    path('myprofile/', views.custom_user_details, name='custom_user_details'),
]
