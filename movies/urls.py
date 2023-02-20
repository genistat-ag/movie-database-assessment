from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review', views.ListReviewAPIView.as_view(), name='get_review'),
    path('<str:pk>/review/', views.CreateReviewAPIView.as_view(), name='create_review'),
    path('review/<str:pk>/', views.RetrieveUpdateDestroyReviewAPIView.as_view(), name='get_delete_update_review'),
]
