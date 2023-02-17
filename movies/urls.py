from django.urls import path
from . import views

app_name = "movies"
urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('own-added-movies/', views.OwnAddedMoviesList.as_view(), name='own_added_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path("review/review-list/",views.ListCreateReviewAPIView.as_view(),name='get_post_review'),
    path('review/<str:pk>/', views.RetrieveUpdateDestroyReviewAPIView.as_view(), name='get_delete_update_review'),
    path('reports/create/', views.ReportCreateView.as_view(), name='report_create'),
    path('reports/report-list/', views.ReportListView.as_view(), name='report_list'),
    path('reports/<str:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<str:pk>/state-change/', views.ReportStateChangeView.as_view(), name='report_state_change'),
    path('reports/<str:pk>/state-undo/',views.ReportStateUndoView.as_view(), name='report_state_undo'),

]