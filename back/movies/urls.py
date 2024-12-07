# movies/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),

    path('<int:movie_pk>/detail/', views.movie_detail),
    path('<int:movie_pk>/wishlist/', views.toggle_wishlist),
    path('<int:movie_pk>/reviews/', views.movie_reviews),
    path('<int:movie_pk>/review/create/', views.create_review),

    path('reviews/<int:review_pk>/', views.review_detail),
    path('reviews/<int:review_pk>/like/', views.toggle_like_review),
    path('reviews/<int:review_pk>/comments/', views.create_comment),
    path('reviews/comments/<int:comment_pk>/', views.comment_detail),

    path('tmdb/<int:tmdb_id>/', views.movie_tmdb),
    path('tmdb/', views.movie_tmdb),
    path('<int:movie_pk>/actors/', views.add_movie_actors),
    path('<int:movie_pk>/genres/', views.add_movie_genres),
    path('<int:movie_pk>/directors/', views.add_movie_directors),

    path('reviews/all/', views.all_reviews),
    path('reviews/latest/<str:username>/', views.user_latest_review),
]

