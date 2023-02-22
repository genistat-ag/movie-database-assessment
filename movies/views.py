from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Movie,Rating,Report
from .serializers import MovieSerializer, ReviewSerializer, MovieRetrieveSerializer, ReportSerializer, ReportRetrieveSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from .permissions import IsOwnerOrReadOnly, IsSuperUser
from rest_framework.permissions import IsAuthenticated

# Removes permissions from views


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Movie.objects.exclude(Q(is_inappropriate=True) & Q(creator=self.request.user))

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieRetrieveSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


class CreateReportAPIView(CreateAPIView):
    serializer_class=ReportSerializer
    queryset=Report.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class VerifyReportAPIView(ListAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class=ReportRetrieveSerializer
    queryset=Report.objects.all()
    permission_classes = (IsSuperUser,)


    