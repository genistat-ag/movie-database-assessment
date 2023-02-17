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

