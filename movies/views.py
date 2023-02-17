from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, 
    ListCreateAPIView,
    RetrieveUpdateAPIView
)
 
from .filters import MovieFilter
from .models import Movie,Rating, Report
from .pagination import CustomPagination
from .serializers import MovieSerializer,ReviewSerializer, ReportSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedAndReviewer, IsSuperuserOrAuthenticatedForGetAndPost, IsSuperuser
from .utils import calculate_move_review_avg, toggle_reported_movie_is_active


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, avg_rating=0)

    def get_queryset(self):
        # Movies that are not user's and are inactive will be excluded. ~Q() Not Equal to
        return super().get_queryset().exclude(~Q(creator_id=self.request.user.id), is_active=False)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    """ GET, UPDATE, DELETE movies """
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class ListCreateReviewAPIView(ListCreateAPIView):
    """LIST, CREATE, GET Reviews"""
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        saved_review = serializer.save(reviewer=self.request.user)
        calculate_move_review_avg(saved_review.movie_id)


class RetrieveUpdateReviewAPIView(RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticatedAndReviewer,)

    def perform_update(self, serializer):
        saved_review = serializer.save(reviewer=self.request.user)
        calculate_move_review_avg(saved_review.movie_id)


class ListCreateReportAPIView(ListCreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsSuperuserOrAuthenticatedForGetAndPost,)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class SuperuserRetrieveUpdateDestroyReportAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsSuperuser,)

    def perform_update(self, serializer):
        reported_object = serializer.save()
        toggle_reported_movie_is_active(reported_object)
    