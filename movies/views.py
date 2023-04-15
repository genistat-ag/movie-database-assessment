from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    ListAPIView,
)
from rest_framework.views import APIView

from django_filters import rest_framework as filters
from .models import Movie,Rating, MovieReport
from .serializers import (
    MovieSerializer,
    ReviewSerializer, 
    MovieReportSerializer,
    MovieDetailSerializer,
)
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly #need to import permission class
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Movie.objects.filter(is_inappropriate=False)

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)

class ListUserOwnMoviesAPIView(ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Movie.objects.filter(creator=self.request.user)

class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)  #permisson neeed to change only owner to update 
    def get_queryset(self):
        return Movie.objects.filter(is_inappropriate=False)


class ListCreateReviewAPIView(ListCreateAPIView):
    """   Create review for a Movie   """

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        movie_id = self.kwargs.get('movie_id')
        return Rating.objects.filter(movie_id=movie_id)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        movie = serializer.validated_data['movie']
        movie.update_avg_rating()


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    """"  User can change their review """

    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsOwnerOrReadOnly,) #permisson neeed to change only owner to update

    def perform_update(self, serializer):
        serializer.save()
        movie = serializer.validated_data['movie']
        movie.update_avg_rating()


class ListCreateReportAPIView(ListCreateAPIView):
    """
    - Only authenticated users can report movies.
    - Only SuperAdmins can request a list of all reports
    """

    serializer_class = MovieReportSerializer
    queryset = MovieReport.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAdminUser]
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class UpdateMovieReportAPIView(APIView):
    serializer_class = MovieReportSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self, report_id):
        return get_object_or_404(MovieReport, id=report_id)
   
    def put(self, request, id):
   
        report = self.get_queryset(report_id= id)

        if 'action' not in request.data:
            return Response({'error': 'Action not specified.'}, status=400)

        if request.data['action'] == MovieReport.MARKED_INAPPROPRIATE:
            report.mark_as_inappropriate()
        elif request.data['action'] == MovieReport.REJECTED:
            report.reject_report()
        elif request.data['action'] == MovieReport.UNRESOLVED:
            report.unresolved_report()
        else:
            return Response({'error': 'Invalid action.'}, status=400)
        
        data = {'id': id, "state":request.data['action']}
        serializer = MovieReportSerializer(report, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)