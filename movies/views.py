from django.db.models import Avg
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView
from django_filters import rest_framework as filters
from .models import Movie,Rating
from .serializers import MovieSerializer,ReviewSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated

from movies.custom_exception import UserNotMatchedException, MyCustomException



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
    
