from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_actor, name='predict_actor'),
]
