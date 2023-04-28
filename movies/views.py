from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, UpdateAPIView, \
    ListAPIView
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .models import Movie, Rating, Report
from .permissions import IsOwnerOrReadOnly, IsReviewerOrReadOnly
from .serializers import MovieSerializer, ReviewSerializer, ReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Removes permissions from views


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all the movies for authenticated user.
        If the user wants to see only his movies, user can add a query parameter to the url: ?search=own
        """
        # If the user wants to see only his movies
        own_movie = self.request.query_params.get('search', None) == 'own'
        if own_movie:
            return Movie.objects.filter(creator=self.request.user)
        return self.queryset.filter(hidden=False)

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)  # Only the creator of the movie can edit it


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsReviewerOrReadOnly)


class ReportMovieView(CreateAPIView):
    """
    API endpoint for authenticated users to report a movie as inappropriate.

    Only authenticated users can report movies.
    """

    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        """
        Report a movie as inappropriate.

        :param request: HTTP request object
        :param movie_id: ID of the movie being reported
        :return: HTTP response with serialized report data
        """
        movie = get_object_or_404(Movie, pk=movie_id)
        report = Report(movie=movie, user=request.user)
        report.save()
        serializer = self.serializer_class(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateReportView(UpdateAPIView):
    """
    API endpoint for SuperAdmins to update the state of a report.

    Only SuperAdmins can request a list of all reports.
    The list should contain the state of the reports.
    Reports are initially in an “unresolved” state.
    SuperAdmin can either set them to “Mark movie as inappropriate” or “Reject report”
    State Management should be implemented with the state machine pattern
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = 'report_id'

    def put(self, request, *args, **kwargs):
        """
        Update the state of a report.

        :param request: HTTP request object
        :param report_id: ID of the report being updated
        :return: HTTP response with serialized report data
        """
        report = self.get_object()
        state = request.data.get('state', None)
        if state is not None and state in ['inappropriate', 'rejected']:
            report.state = state
            report.save()
            if state == 'inappropriate':
                report.movie.hidden = True
                report.movie.save()
            elif report.movie.hidden:
                report.movie.hidden = False
                report.movie.save()
        serializer = self.serializer_class(report)
        return Response(serializer.data)


class ReportListView(ListAPIView):
    """
    API endpoint for SuperAdmins to view a list of all reports.

    Only SuperAdmins can request a list of all reports.
    The list should contain the state of the reports.
    """

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Get a list of all reports.

        :param request: HTTP request object
        :return: HTTP response with serialized report data
        """
        return super().get(request, *args, **kwargs)
