from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('<int:movie_pk>/detail/', views.movie_detail),
    path('<int:movie_pk>/review/<int:review_pk>/', views.review_handler),
    path('<int:movie_pk>/review/<int:review_pk>/comment/', views.comment_handler),
]
