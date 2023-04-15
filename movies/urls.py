from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review',views.ListCreateReviewAPIView.as_view(),name='get_post_review'),
    path('review/<int:pk>/',views.RetrieveUpdateDestroyReviewAPIView.as_view(),name='get_delete_update_review'),

    path('me', views.ListUserOwnMoviesAPIView.as_view(), name='get_user_own_movies'),
]