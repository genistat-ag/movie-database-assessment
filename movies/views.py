from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from .models import Movie,Rating
from .serializers import MovieSerializer,ReviewSerializer, MovieReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
from rest_framework.permissions import BasePermission, SAFE_METHODS

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


class IsCreatorOrAuthenticatedReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request method is a safe method (i.e., GET, HEAD, or OPTIONS)
        if request.method in SAFE_METHODS:
            # Allow authenticated users to read the object
            return True
        # Check if the creator of the object is the same as the user making the request
        return obj.creator == request.user

class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsCreatorOrAuthenticatedReadOnly)


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def validate_score(self, score):
        if score>5 or score<1:
            raise ValidationError('Rating range is 1-5 inclusive')

    def perform_create(self, serializer):
        score = self.request.data.get('score')
        movie_id = self.request.data.get('movie')
        reviewer_id = self.request.user.id
        self.validate_score(score)
        is_rating_exist_for_same_movie = Rating.objects.filter(movie_id=movie_id, reviewer_id=reviewer_id).exists()
        if is_rating_exist_for_same_movie:
            raise ValidationError('You have already rated this movie')

        serializer.save(reviewer=self.request.user)
        self.update_movie_rating_avg(movie_id)

    def update_movie_rating_avg(self, movie_id):
        movie_id = Movie.objects.get(id=movie_id)
        ratings = Rating.objects.filter(movie=movie_id)
        total_rating = ratings.aggregate(total = Sum("score"))
        avg_rating = total_rating['total']/ratings.count()
        movie_id.avg_rating = avg_rating
        movie_id.save()


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsCreatorOrAuthenticatedReadOnly)
    lookup_field = 'movie_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(movie__id=self.kwargs['movie_id'], reviewer_id=self.request.user)


class ListCreateMovieReportAPIView(ListCreateAPIView):
    serializer_class = MovieReportSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

