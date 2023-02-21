from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)

from .utils import calculate_movie_review_avg
from .models import Movie,Rating
from .serializers import MovieSerializer,ReviewSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from .permissions import IsOwnerOrReadOnly, IsReviewerOrReadOnly


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, avg_rating=0)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        saved_review = serializer.save(reviewer=self.request.user)
        calculate_movie_review_avg(saved_review.movie_id)


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsReviewerOrReadOnly)

    def perform_update(self, serializer):
        saved_review = serializer.save(reviewer=self.request.user)
        calculate_movie_review_avg(saved_review.movie_id)
