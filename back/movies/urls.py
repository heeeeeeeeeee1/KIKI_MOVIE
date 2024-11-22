from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),
    path('<int:movie_pk>/detail/', views.movie_detail),
    path('<int:movie_pk>/review/<int:review_pk>/', views.movie_review),
    path('<int:movie_pk>/review/create/', views.review_create, name='review-create'),
    path('<int:movie_pk>/review/<int:review_pk>/comment/create/', views.comment_create, name='comment-create'),

]
