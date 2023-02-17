from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review/rating/',views.ListCreateReviewAPIView.as_view(),name='get_post_reviews'),
    path('review/rating/<pk>/',views.RetrieveUpdateDestroyRatingAPIView.as_view(),name='get_delete_update_rating'),
    path('movie/report/',views.ListCreateReportAPIView.as_view(),name='get_post_reposrts'),
    path('movie/report/<pk>/',views.RetrieveUpdateDestroyReportAPIView.as_view(),name='get_delete_update_report')
]