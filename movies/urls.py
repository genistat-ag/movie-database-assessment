from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.ListCreateReviewAPIView.as_view(), name='get_post_review'),
    path('review/<str:pk>/', views.RetrieveUpdateDestroyReviewAPIView.as_view(), name='get_delete_update_review'),
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
]
