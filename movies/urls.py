from django.urls import path
from . import views

# 
urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('review/', views.ListCreateReviewAPIView.as_view(), name='get_post_review'),
    path('review/<str:pk>/', views.RetrieveUpdateReviewAPIView.as_view(), name='get_delete_update_review'),
    path('report/', views.ListCreateReportAPIView.as_view(), name='get_post_movie_report'),
    path('report/<str:pk>/', views.SuperuserRetrieveUpdateDestroyReportAPIView.as_view(), name='movie_report_update_destroy'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
]