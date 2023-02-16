from django.urls import path
from . import views


urlpatterns = [

    # for movie
    path('movie/create-or-list', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('movie/own/list', views.OwnMovieListView.as_view(), name='own_movies'),
    path('movie/<str:pk>/up-del-retr', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='retr_del_update_movie'),

    # for review or ratting
    path('review/create-or-list', views.ListCreateReviewAPIView.as_view(),name='get_post_review'),
    path('review/<int:pk>/change/', views.ReviewUpdateDestroyAPIView.as_view(),name='review_change'),

    # for report
    path('report/create', views.ReportCreateAPIView.as_view(), name='report_create'),
    path('report/list', views.ReportListAPIView.as_view(), name='report_list'),
    path('report/<int:pk>/change', views.ReportUpdateAPIView.as_view(), name='report_change'),
]