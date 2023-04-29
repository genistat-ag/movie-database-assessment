from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.ListCreateMovieAPIView.as_view()),
    re_path(r'^(?P<pk>[0-9]+)/$',
            views.RetrieveUpdateDestroyMovieAPIView.as_view()),
    re_path(r'^user/?$', views.UserMovieAPIView.as_view()),
    re_path(r'^review/?$', views.ListCreateReviewAPIView.as_view()),
    re_path(r'^review/(?P<pk>[0-9]+)/$',
            views.RetrieveUpdateDestroyReviewAPIView.as_view()),
    re_path(r'^report/?$', views.ListCreateReportAPIView.as_view()),
    re_path(r'^report/(?P<pk>[0-9]+)/$',
            views.RetrieveUpdateDestroyReportAPIView.as_view()),
]
