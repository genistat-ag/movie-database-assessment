from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('movies/<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('reviews/', views.ListCreateReviewAPIView.as_view(), name='get_post_review'),
    path('movies/reviews/<str:pk>/', views.RetrieveUpdateDestroyReviewAPIView.as_view(), name='get_delete_update_review'),
    path('reports/', views.ListCreateReportAPIView.as_view(), name='create-report'),
    path('movies/report/<str:pk>/approve/', views.ApproveReportAPIView.as_view(), name='approved-report'),
    path('movies/report/<str:pk>/reject/', views.RejectReportAPIView.as_view(), name='reject-report'),
    path('movies/report/<str:pk>/approve_to_reject/', views.ApproveToRejectReportAPIView.as_view(), name='reject-report'),
    path('movies/report/<str:pk>/reject_to_approve/', views.RejectToApproveReportAPIView.as_view(), name='reject-report'),
]
