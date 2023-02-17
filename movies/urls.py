from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<int:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review/',views.ListCreateReviewAPIView.as_view(), name='get_post_review'),
    path('review/<int:pk>/',views.RetrieveUpdateReviewAPIView.as_view(), name='get_update_review'),

    path('report',views.ListCreateReportAPIView.as_view(),name='get_report'),
]