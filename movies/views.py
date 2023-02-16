from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, get_object_or_404
from django_filters import rest_framework as filters
from .models import Movie,Rating
from .serializers import MovieSerializer,ReviewSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated


class ListCreateMovieAPIView(ListCreateAPIView):
    """ Here, authenticated users can see all movies for get request"""
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
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """ A movie can only be updated by its creator. """
        if self.request.method in ['PUT', 'PATCH']:
            return get_object_or_404(Movie, creator=self.request.user, id=self.kwargs.get("pk"))
        return super().get_object()


class ListCreateReviewAPIView(ListCreateAPIView):
    """ Only authenticated users can give ratings. """

    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

