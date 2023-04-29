from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .filters import MovieFilter
from .models import Movie, Rating
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import MovieSerializer, ReviewSerializer


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

    # bug: filtering not done for inappropriate movies when user is not creator
    def get_queryset(self):
        query = super().get_queryset()
        ids = []
        for i in query:
            if i.status == "inappropriate":
                if i.creator == self.request.user:
                    ids.append(i.id)
            else:
                ids.append(i.id)
        return query.filter(id__in=ids)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)  # bug: only owner can update or delete movie
    http_method_names = ["get", "put", "delete"]  # restrict available methods


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # update: reivewer -> creator for field name as modified in model
        serializer.save(creator=self.request.user)


# new: endpoints to read or update reviews
class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ["get", "put", "delete"]
