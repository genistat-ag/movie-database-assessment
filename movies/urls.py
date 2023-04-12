from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<int:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('reports/', views.ListCreateReportAPIView.as_view(), name='get_post_reports'),
    path('reports/<int:pk>/', views.RetrieveUpdateDestroyReportAPIView.as_view(), name='get_delete_update_reports'),
    path('reviews/',views.ListCreateReviewAPIView.as_view(), name='get_post_review'),
    path('reviews/<int:pk>/',views.RetrieveUpdateDestroyReviewAPIView.as_view(), name='get_delete_update_review'),
]