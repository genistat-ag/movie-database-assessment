from django.db.models import Avg, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating, Report
from .serializers import MovieSerializer, ReviewSerializer, ReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from movies.custom_exception import UserNotMatchedException, MyCustomException



# Removes permissions from views


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        '''
        This query will filter all unappropriate movie
        but movie will show to the creator despite unappropriate
        '''
        q1 = Report.objects.filter(Q(state=Report.INAPPROPRIATE_MOVIE) ).values('movie_id').all()

        movie_ids = [report['movie_id'] for report in q1]

        return Movie.objects.filter(~Q(id__in=movie_ids) | Q(creator=self.request.user))


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()


        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.creator != request.user:
            raise UserNotMatchedException(
                'current user does not have permission to perform this action!'
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListCreateUpdateReviewAPIView(ListCreateAPIView, UpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def update_movie_rating(self, movie_id):
        avg_value = Rating.objects.filter(movie=movie_id).aggregate(Avg('score')).get('score__avg')
        
        movie_obj = Movie.objects.get(pk=movie_id)
        movie_obj.avg_rating = avg_value
        movie_obj.save(update_fields=['avg_rating'])
        

    def _check_score_validity(self, score):
        if score < 1 or score > 5:
            raise MyCustomException('Rating can not be less than 1 and more than 5')

    def perform_create(self, serializer):
        score = self.request.data.get('score')
        self._check_score_validity(score)
 
        serializer.save(reviewer=self.request.user)

        self.update_movie_rating(serializer.data.get('movie'))


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.reviewer != request.user:
            raise MyCustomException(
                'current user does not have permission to perform this action!'
            )

        score = request.data.get('score')
        self._check_score_validity(score)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)


        self.perform_update(serializer)

        self.update_movie_rating(request.data.get('movie'))

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ListCreateUpdateReportAPIView(ListCreateAPIView, UpdateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_permissions(self):
        method = self.request.method
        return [IsAdminUser(), ] if method in ['GET','PUT'] else [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):

        reporter = self.request.user
        serializer.save(reporter=reporter)
