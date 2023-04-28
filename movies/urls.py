from django.urls import path
from . import views
from .views import ReportMovieView, UpdateReportView, ReportListView

urlpatterns = [
    path('', views.ListCreateMovieAPIView.as_view(), name='get_post_movies'),
    path('<str:pk>/', views.RetrieveUpdateDestroyMovieAPIView.as_view(), name='get_delete_update_movie'),
    path('review', views.ListCreateReviewAPIView.as_view(),name='get_post_review'),
    path('review/<str:pk>/', views.RetrieveUpdateDestroyReviewAPIView.as_view(), name='get_delete_update_review'),

    path('<int:movie_id>/report/', ReportMovieView.as_view(), name='report_movie'), # any user can report a movie
    path('reports/<int:report_id>/', UpdateReportView.as_view(), name='update_report'), # only superadmins can update a report
    path('reports/all/', ReportListView.as_view(), name='report_list'), # only superadmins can view all reports
]