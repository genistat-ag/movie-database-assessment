from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from django_filters import rest_framework as filters
from .models import Movie, Rating
from .serializers import MovieSerializer, ReviewSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Movie.objects.filter(creator=self.request.user)
        else:
            return Movie.objects.all()


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Movie.objects.filter(creator=self.request.user)
        else:
            return Movie.objects.all()


class ListMoviesAPIView(ListAPIView):
    serializer_class = MovieSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        return Movie.objects.all()


class RetrieveMovieAPIView(RetrieveAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        return Movie.objects.all()


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
