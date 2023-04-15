from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
)
from django_filters import rest_framework as filters
from .models import Movie,Rating
from .serializers import (
    MovieSerializer,
    ReviewSerializer,
    MovieDetailSerializer,
)
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly #need to import permission class

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

class ListUserOwnMoviesAPIView(ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Movie.objects.filter(creator=self.request.user)

class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)  #permisson neeed to change only owner to update 
    def get_queryset(self):
        return Movie.objects.filter()


class ListCreateReviewAPIView(ListCreateAPIView):
    """   Create review for a Movie   """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return Rating.objects.filter(movie_id=movie_id)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        movie = serializer.validated_data['movie']
        movie.update_avg_rating()


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    """"  User can change their review """

    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsOwnerOrReadOnly,) #permisson neeed to change only owner to update

    def perform_update(self, serializer):
        serializer.save()
        movie = serializer.validated_data['movie']
        movie.update_avg_rating()
