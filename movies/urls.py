from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review',views.ListCreateReviewAPIView.as_view(),name='get_post_review'),
    path('review/<str:pk>/',views.RetrieveUpdateDestroyReviewAPIView.as_view(),name='get_post_review'),
    path('report', views.ListCreateReportAPIView.as_view(), name='create-report'),
    path('report/<str:pk>/approve', views.ApproveReportAPIView.as_view(), name='approved-report'),
    path('report/<str:pk>/reject', views.RejectReportAPIView.as_view(), name='reject-report'),
    path('report/<str:pk>/approve_to_reject', views.ApproveToRejectReportAPIView.as_view(), name='reject-report'),
    path('report/<str:pk>/reject_to_approve', views.RejectToApproveReportAPIView.as_view(), name='reject-report'),
]