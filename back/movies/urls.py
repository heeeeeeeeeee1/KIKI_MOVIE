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

    # path('movies/<int:movie_pk>/reviews/<int:review_pk>/comment/', views.comment_detail),
    # path('movies/<int:movie_pk>/reviews/<int:review_pk>/comment/<int:comment_pk>/', views.comment_detail),

    # path('<int:movie_pk>/review/<int:review_pk>/', views.movie_review),
    # path('review/<int:review_pk>/like/', views.toggle_like_review),
    # CONFLICT > path('<int:movie_pk>/review/<int:review_pk>/', views.review_handler),
    # CONFLICT > path('<int:movie_pk>/review/<int:review_pk>/comment/', views.comment_handler),
]

