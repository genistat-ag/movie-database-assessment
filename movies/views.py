from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating
from .serializers import MovieSerializer,ReviewSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated, BasePermission

from django.db.models import Avg


# Removes permissions from views

class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user

class IsReviewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user

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
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsAuthenticated(), IsCreator()]
        return [IsAuthenticated()]


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
        # Update movie's average rating
        movie_id = serializer.validated_data['movie'].id
        movie = Movie.objects.get(id=movie_id)
        movie.avg_rating = Rating.objects.filter(movie=movie).aggregate(avg_rating=Avg('score'))['avg_rating']
        movie.save()
    
    def get_object(self):
        obj = super().get_object()
        if self.request.method in ('PUT', 'PATCH', 'DELETE') and obj.reviewer != self.request.user:
            self.permission_denied(self.request, message='You cannot update another user\'s review')
        return obj


class RetrieveUpdateReviewAPIView(RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsAuthenticated(), IsReviewer()]
        return [IsAuthenticated()]
    
    def perform_update(self, serializer):
        serializer.save()
        # Update movie's average rating
        movie_id = serializer.validated_data['movie'].id
        movie = Movie.objects.get(id=movie_id)
        movie.avg_rating = Rating.objects.filter(movie=movie).aggregate(avg_rating=Avg('score'))['avg_rating']
        movie.save()
