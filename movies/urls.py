from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review', views.ListReviewAPIView.as_view(), name='get_review'),
    path('<str:pk>/review/', views.CreateReviewAPIView.as_view(), name='post_review'),
    path('review/<str:pk>/', views.RetrieveUpdateDestroyReviewAPIView.as_view(), name='get_delete_update_review'),
    path('<str:pk>/report/', views.CreateReportAPIView.as_view(), name='post_report'),
    path('report', views.ListReportAPIView.as_view(), name='get_report'),
    path('report/<str:pk>/', views.RetrieveUpdateDestroyReportAPIView.as_view(), name='get_delete_update_report'),
]
