from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, CreateAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating, Report
from .serializers import MovieSerializer, MovieDetailSerializer, ReviewSerializer, ReportSerializer, \
    ReportDetailSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from .permissions import IsOwnerOrReadOnlyMovie, IsOwnerOrReadOnlyReview
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Removes permissions from views

"""
# Movie create & List of movie
# Filter movie of inappropriate tag by conditions
"""


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

    def get_queryset(self):
        if self.request.user.is_staff:  # admin can see all movies
            return self.queryset
        elif not self.request.user.is_staff:  # normal user but movie creator can see also "inappropriate" tag movie
            return self.queryset.filter(Q(report__state__icontains='inappropriate') & Q(creator=self.request.user) | ~Q(
                report__state__icontains='inappropriate'))
        else:  # otherwise "inappropriate" tag movie will be excluded
            return self.queryset.exclude(Q(report__state__icontains='inappropriate'))


""" 
Movie detail/update/destroy
"""


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyMovie)

    def get_queryset(self):
        queryset = Movie.objects.all()
        return queryset


""" 
List of all movie ratings
"""


class ListReviewAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)


""" 
# create movie rating
# update avg_rating in movie
"""


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
        movie.save(update_fields=['avg_rating'])
        serializer.save(movie=movie, reviewer=reviewer)


""" 
rating detail/update/destroy
"""


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
            movie_queryset.save(update_fields=['avg_rating'])
        serializer.save(movie=movie_queryset, reviewer=reviewer)


""" 
User can report a movie
"""


class CreateReportAPIView(CreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=pk)
        reporter = self.request.user
        serializer.save(movie=movie, reporter=reporter)


""" 
All reports for only admin
"""


class ListReportAPIView(ListAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAdminUser,)


"""" 
# report detail/update/destroy
# if movie is "Reject report" then the report will be close/deleted
"""


class RetrieveUpdateDestroyReportAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReportDetailSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAdminUser,)

    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')
        report = Report.objects.get(pk=pk)
        if report:
            if serializer.validated_data['state'] == 'Reject report':
                report.delete()
            else:
                serializer.save(state=serializer.validated_data['state'])
