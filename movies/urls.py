from django.urls import path

from .views import (
    ListCreateMovieAPIView,
    ListCreateReviewAPIView,
    RetrieveUpdateDestroyMovieAPIView,
    RetrieveUpdateDestroyReviewAPIView,
)

urlpatterns = [
    path("", ListCreateMovieAPIView.as_view(), name="get_post_movies"),
    path("<str:pk>/", RetrieveUpdateDestroyMovieAPIView.as_view(), name="get_delete_update_movie"),
    path("review", ListCreateReviewAPIView.as_view(), name="get_post_review"),
    # new: add remaining routes
    path("review/<str:pk>/", RetrieveUpdateDestroyReviewAPIView.as_view(), name="get_post_review"),
]
