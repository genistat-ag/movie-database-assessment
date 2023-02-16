from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<int:pk>/', views.UpdateMovieAPIView.as_view(), name='update_movie'),

    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review',views.ListCreateReviewAPIView.as_view(), name='get_post_review')
]