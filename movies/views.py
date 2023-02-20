from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating, Report
from .serializers import MovieSerializer, MovieDetailSerializer, ReviewSerializer, ReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from .permissions import IsOwnerOrReadOnlyMovie, IsOwnerOrReadOnlyReview
from rest_framework.permissions import IsAuthenticated, IsAdminUser


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
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyMovie)

    def get_queryset(self):
        queryset = Movie.objects.all()
        return queryset


class ListReviewAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)


class CreateReviewAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=pk)
        reviewer = self.request.user
        rating_queryset = Rating.objects.filter(movie=movie,
                                                reviewer=reviewer)
        if rating_queryset.exists():  # if user already posted the review
            return Response({'message': 'You already posted the review for the same movie.!!!'},
                            status=status.HTTP_200_OK)
        if movie.avg_rating == 0:  # if no review is posted yet
            movie.avg_rating = serializer.validated_data['score']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['score']) / 2
        movie.save()
        serializer.save(movie=movie, reviewer=reviewer)


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyReview)

    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')
        rating_queryset = Rating.objects.get(pk=pk)
        movie_queryset = Movie.objects.get(pk=rating_queryset.movie.id)
        reviewer = self.request.user
        if rating_queryset:
            movie_queryset.avg_rating = (movie_queryset.avg_rating + serializer.validated_data['score']) / 2
            movie_queryset.save()
        serializer.save(movie=movie_queryset, reviewer=reviewer)


class CreateReportAPIView(CreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=pk)
        reporter = self.request.user
        serializer.save(movie=movie, reporter=reporter)


class ListReportAPIView(ListAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAdminUser,)
