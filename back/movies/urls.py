from django.urls import path
from . import views

urlpatterns = [
    path('/<int:movie_pk>/detail', views.detail),
    path('/<int:movie_pk>/review/<int:review_pk>', views.review),       
]
