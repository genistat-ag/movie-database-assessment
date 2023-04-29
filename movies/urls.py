from django.urls import path

from .views import (
    ApproveReportAPIView,
    ApproveToRejectReportAPIView,
    ListCreateMovieAPIView,
    ListCreateReportAPIView,
    ListCreateReviewAPIView,
    RejectReportAPIView,
    RejectToApproveReportAPIView,
    RetrieveUpdateDestroyMovieAPIView,
    RetrieveUpdateDestroyReviewAPIView,
)

urlpatterns = [
    path("", ListCreateMovieAPIView.as_view(), name="get_post_movies"),
    path("<str:pk>/", RetrieveUpdateDestroyMovieAPIView.as_view(), name="get_delete_update_movie"),
    path("review", ListCreateReviewAPIView.as_view(), name="get_post_review"),
    # new: add remaining routes
    path("review/<str:pk>/", RetrieveUpdateDestroyReviewAPIView.as_view(), name="get_post_review"),
    path("report", ListCreateReportAPIView.as_view(), name="get_post_report"),
    path("report/<str:pk>/approve", ApproveReportAPIView.as_view(), name="approve_report"),
    path("report/<str:pk>/reject", RejectReportAPIView.as_view(), name="reject_report"),
    path("report/<str:pk>/approve-to-reject", ApproveToRejectReportAPIView.as_view(), name="reject_report"),
    path("report/<str:pk>/reject-to-approve", RejectToApproveReportAPIView.as_view(), name="reject_report"),
]
