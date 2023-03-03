from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.ListMoviesAPIView.as_view(), name="list_movies"),
    path("movies/<int:pk>/", views.RetrieveMovieAPIView.as_view(), name="get_movie"),
    path(
        "my-movies/", views.ListCreateMovieAPIView.as_view(), name="get_post_my_movies"
    ),
    path(
        "my-movies/<int:pk>/",
        views.RetrieveUpdateDestroyMovieAPIView.as_view(),
        name="get_delete_update_my_movie",
    ),
    path("reviews/", views.ListCreateReviewAPIView.as_view(), name="get_post_review"),
]
