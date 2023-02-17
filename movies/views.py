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
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MovieDetailsSerializer(instance)
        return Response(serializer.data)


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    http_method_names = ['get', 'post', 'patch']
    permission_classes = (IsAuthenticated, HasMoviePermission,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Report.objects.all()
        else:
            return Report.objects.filter(reporter=user)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @action(detail=True, methods=['patch'], url_path='mark-inappropriate')
    def mark_as_inappropriate(self, request, pk=None):
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
        report = self.get_object()
        if report.state != State.UNRESOLVED:
            return Response({"detail": "Report has already been resolved"}, status=status.HTTP_400_BAD_REQUEST)
        report.set_state(State.REJECT_REPORT)
        return Response(self.get_serializer(report).data)

    @action(detail=True, methods=['patch'], url_path='revert')
    def revert_report(self, request, pk=None):
        report = self.get_object()
        if report.state == State.UNRESOLVED:
            return Response({"detail": "Report hasn't been resolve yet"}, status=status.HTTP_400_BAD_REQUEST)
        report.set_state(State.UNRESOLVED)
        return Response(self.get_serializer(report).data)
