from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('own/', views.OwnMovieListView.as_view(), name='own_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review', views.ListCreateReviewAPIView.as_view(),name='get_post_review'),
    path('review/<int:pk>/change/', views.ReviewUpdateDestroyAPIView.as_view(),name='review_change'),

    path('report/create', views.ReportCreateAPIView.as_view(), name='report_create'),
    path('report/list', views.ReportListAPIView.as_view(), name='report_list'),
    path('report/<int:pk>/change', views.ReportUpdateAPIView.as_view(), name='report_change'),
]