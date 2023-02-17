from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from django_filters import rest_framework as filters
from .models import Movie,Rating, Report
from .serializers import MovieSerializer,ReviewSerializer, ReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import IsSuperAdmin
from rest_framework import generics, status

# Removes permissions from views


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]


    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]
    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        if movie.creator != self.request.user:
            raise PermissionDenied("You do not have permission to update this movie.")
        return super().update(request, *args, **kwargs)


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]

    def perform_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=self.request.user)
        movie = serializer.validated_data['movie']
        ratings = Rating.objects.filter(movie=movie.id)
        movie_model = Movie.objects.get(id=movie.id)
        count = ratings.count()
        total_rating = sum(rating.score for rating in ratings)
        average_rating = total_rating / count if count > 0 else 0
        movie_model.avg_rating = average_rating
        movie_model.save()

class OwnAddedMoviesList(ListAPIView):
    serializer_class = MovieSerializer
    def get_queryset(self):
        user = self.request.user
        return Movie.objects.filter(creator = user)
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]

class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.reviewer != self.request.user:
            raise PermissionDenied("You do not have permission to update this rating because you are not the creator of this review.")
        serializer = self.get_serializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ratings = Rating.objects.filter(id=review.id)
        count = ratings.count()
        total_rating = sum(rating.score for rating in ratings)
        average_rating = total_rating / count if count > 0 else 0
        Movie.objects.filter(id=review.movie.id).update(avg_rating=average_rating)
        return super().update(request, *args, **kwargs)

class ReportCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = ReportSerializer

class ReportListView(generics.ListAPIView):
    print("------------------")
    permission_classes = [IsSuperAdmin]
    authentication_classes = [SessionAuthentication]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    print(queryset)

class ReportDetailView(generics.RetrieveAPIView):
    permission_classes = [IsSuperAdmin]
    authentication_classes = [SessionAuthentication]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportStateChangeView(APIView):
    permission_classes = [IsSuperAdmin]
    authentication_classes = [SessionAuthentication]

    def patch(self, request, pk):
        report = Report.objects.get(pk=pk)
        previous_state = report.state
        report.mark_inappropriate()
        report.save()
        return Response({'message': f'Report state changed from {previous_state} to {report.state}'}, status=status.HTTP_200_OK)

class ReportStateUndoView(APIView):
    permission_classes = [IsSuperAdmin]

    def patch(self, request, pk):
        report = Report.objects.get(pk=pk)
        previous_state = report.state
        report.unmark_inappropriate()
        report.save()
        return Response({'message': f'Report state changed from {previous_state} to {report.state}'}, status=status.HTTP_200_OK)


