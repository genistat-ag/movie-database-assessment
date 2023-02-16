from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from .models import Movie,Rating
from .permissions import IsOwnerOrReadOnly
from .serializers import MovieSerializer,ReviewSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated

# Removes permissions from views


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)


    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

