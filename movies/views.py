from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .models import Movie, Rating, Report, State
from .permissions import IsOwnerOrReadOnly, HasMoviePermission
from .serializers import MovieSerializer, ReviewSerializer, MovieDetailsSerializer, ReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated


class ListCreateMovieAPIView(ListCreateAPIView):
    """
     API view for listing and creating movies.

     Attributes:
    - serializer_class: A serializer class for the movie model.
    - queryset: A queryset of all movies.
    - pagination_class: A custom pagination class.
    - filter_backends: A tuple of filter backends to be used.
    - filterset_class: A filter class for the movie model.
    - permission_classes: A tuple of permission classes for the view.
     """
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Returns a filtered queryset of movies.

        If the user is authenticated, the queryset will include movies that belong to the user and have the
        is_inappropriate flag set to True, in addition to all movies that do not have this flag set. If the user is
        a superuser, all movies will be included in the queryset.

        Returns:
        -  A filtered queryset of movies.
        """
        user = self.request.user
        queryset = Movie.objects.filter(is_inappropriate=False)

        # Show creator's is_inappropriate=True movies
        if user.is_authenticated:
            creator_movies = Movie.objects.filter(creator=user, is_inappropriate=True)
            queryset = creator_movies | queryset

        if user.is_superuser:
            queryset = Movie.objects.all()

        return queryset

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a single movie.

    Attributes:
    - serializer_class: A serializer class for the movie model.
    - queryset: A queryset of all movies.
    - permission_classes: A tuple of permission classes for the view.
    """
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MovieDetailsSerializer(instance)
        return Response(serializer.data)


class ListCreateReviewAPIView(ListCreateAPIView):
    """
    API view for listing and creating reviews.

    Attributes:
    - serializer_class: A serializer class for the review model.
    - queryset: A queryset of all ratings.
    - permission_classes: A tuple of permission classes for the view.
    - pagination_class: A custom pagination class.
    """
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a single review.

    Attributes:
    - serializer_class: A serializer class for the review model.
    - queryset: A queryset of all ratings.
    - permission_classes: A tuple of permission classes for the view.
    """
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)


class ReportViewSet(viewsets.ModelViewSet):
    """
    API view for managing reports.

    Attributes:
    - serializer_class: A serializer class for the report model.
    - queryset: A queryset of all reports.
    - http_method_names: A list of HTTP methods allowed for the view.
    - permission_classes: A tuple of permission classes for the view.
    - pagination_class: A custom pagination class.
    """

    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    http_method_names = ['get', 'post', 'patch']
    permission_classes = (IsAuthenticated, HasMoviePermission,)
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Returns a queryset of all reports that the user is allowed to see.

        Returns:
        - A queryset of reports.
        """
        user = self.request.user
        if user.is_superuser:
            return Report.objects.all()
        else:
            return Report.objects.filter(reporter=user)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @action(detail=True, methods=['patch'], url_path='mark-inappropriate')
    def mark_as_inappropriate(self, request, pk=None):
        """
        Marks a report as inappropriate and hides the associated movie.

        Args:
        - request: The HTTP request object.
        - pk: The primary key of the report.

        Returns:
        - A response with the serialized report data.
        """
        report = self.get_object()
        if report.state != State.UNRESOLVED:
            return Response({"detail": "Report has already been resolved"}, status=status.HTTP_400_BAD_REQUEST)

        # set_state the selected report to MARK_AS_INAPPROPRIATE state
        report.set_state(State.MARK_AS_INAPPROPRIATE)
        report.save()

        # Mark movie as inappropriate and hide it from all users
        movie = report.movie
        movie.is_inappropriate = True
        movie.save()

        return Response(self.get_serializer(report).data)

    @action(detail=True, methods=['patch'], url_path='reject')
    def reject_report(self, request, pk=None):
        """
        Rejects a report.

        Args:
        - request: The HTTP request object.
        - pk: The primary key of the report.

        Returns:
        - A response with the serialized report data.
        """
        report = self.get_object()
        if report.state != State.UNRESOLVED:
            return Response({"detail": "Report has already been resolved"}, status=status.HTTP_400_BAD_REQUEST)
        report.set_state(State.REJECT_REPORT)
        return Response(self.get_serializer(report).data)

    @action(detail=True, methods=['patch'], url_path='revert')
    def revert_report(self, request, pk=None):
        """
        Reverts a report to the UNRESOLVED state.

        Args:
        - request: The HTTP request object.
        - pk: The primary key of the report.

        Returns:
        - A response with the serialized report data.
        """
        report = self.get_object()
        if report.state == State.UNRESOLVED:
            return Response({"detail": "Report hasn't been resolve yet"}, status=status.HTTP_400_BAD_REQUEST)
        report.set_state(State.UNRESOLVED)
        return Response(self.get_serializer(report).data)
