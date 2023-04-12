from django.urls import path
from . import views


urlpatterns = [
    # path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    # path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    # path('review', views.ListCreateReviewAPIView.as_view(), name='get_post_review')
    path("", views.MoviesAPIView.as_view(), name="movies"),
    path("<str:pk>/", views.MoviesDetailsAPIView.as_view(), name="movie-details"),
    path("created-by-me", views.OwnMoviesAPIView.as_view(), name="created-by-me"),
    path("rating", views.RatingAPIView.as_view(), name="rating"),
    path("rating/<str:pk>/", views.RatingDetailsAPIView.as_view(), name="rating-details"),
    path("reports", views.ReportedMoviesListAPIView.as_view(), name="report-movie"),
]