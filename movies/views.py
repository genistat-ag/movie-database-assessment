from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating, ReportMovie
from .serializers import MovieSerializer, ReviewSerializer, ReportMovieSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class MoviesAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer

    def get(self, request):
        try:
            movies = Movie.objects.exclude(state="make movie as inappropriate")
            movie_serializer = self.serializer_class(movies, many=True)
            return Response({
                "data": movie_serializer.data,
                "response_code": status.HTTP_200_OK,
                "response_message": "success"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {},
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": e.args[0]
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        payload = request.data
        movie_serializer = self.serializer_class(data=payload)
        if movie_serializer.is_valid():
            movie_serializer.save(creator=request.user)
            return Response({
                "data": movie_serializer.data,
                "response_code": status.HTTP_201_CREATED,
                "response_message": "success"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "data": movie_serializer.errors,
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": "success"
            }, status=status.HTTP_400_BAD_REQUEST)


class MoviesDetailsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer

    def get(self, request, pk):
        movie = Movie.objects.filter(id=pk).last()
        if not movie:
            return Response({
                "data": {},
                "response_code": status.HTTP_204_NO_CONTENT,
                "response_message": "no content"
            }, status=status.HTTP_204_NO_CONTENT)

        movie_serializer = self.serializer_class(movie)
        return Response({
            "data": movie_serializer.data,
            "response_code": status.HTTP_200_OK,
            "response_message": "success"
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = Movie.objects.filter(creator=request.user, id=pk).last()
        if not movie:
            return Response({
                "data": {},
                "response_code": status.HTTP_204_NO_CONTENT,
                "response_message": "no content"
            }, status=status.HTTP_204_NO_CONTENT)

        payload = request.data
        movie_serializer = self.serializer_class(movie, data=payload)
        if movie_serializer.is_valid():
            movie_serializer.save(creator=request.user)
            # movie rating initialization
            movie_rating = Rating(movie=movie, reviewer=request.user, score=0)
            movie_rating.save()
            return Response({
                "data": movie_serializer.data,
                "response_code": status.HTTP_200_OK,
                "response_message": "success"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "data": movie_serializer.errors,
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": "success"
            }, status=status.HTTP_400_BAD_REQUEST)


class OwnMoviesAPIView(GenericAPIView):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # movies created by the user
            movies = Movie.objects.filter(creator=request.user)
            movie_serializer = self.serializer_class(movies, many=True)
            return Response({
                "data": movie_serializer.data,
                "response_code": status.HTTP_200_OK,
                "response_message": "success"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {},
                "response_code": status.HTTP_400_BAD_REQUEST,
                "response_message": e.args[0]
            }, status=status.HTTP_400_BAD_REQUEST)


class RatingAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get(self, request):
        movie_id = request.query_params.get("movie_id")
        ratings = Rating.objects.filter(movie__id=movie_id)
        rating_serializer = self.serializer_class(ratings, many=True)
        return Response({
            "data": rating_serializer.data,
            "response_code": status.HTTP_200_OK,
            "response_message": "success"
        }, status=status.HTTP_200_OK)

    def post(self, request):
        movie_id = request.query_params.get("movie_id")
        payload = request.data
        rating = Rating.objects.filter(movie__id=movie_id).last()
        if payload["rating"] < 1 or payload["rating"] > 5:
            return Response({
                "data": {},
                "response_code": status.HTTP_409_CONFLICT,
                "response_message": "rating out of range"
            }, status=status)

        rating.score = payload["rating"]
        rating.save()
        # get total rating of this movie
        total_rating_count = Rating.objects.filter(movie__id=movie_id).count()
        total_rating = 0
        for rating in Rating.objects.filter(movie__id=movie_id):
            total_rating += rating.score

        avg_rating = total_rating / total_rating_count
        movie = Movie.objects.filter(id=movie_id).last()
        movie.avg_rating = avg_rating
        movie.save()
        return Response({
            "data": {},
            "response_code": status.HTTP_200_OK,
            "response_message": "success"
        }, status=status.HTTP_200_OK)


class RatingDetailsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def put(self, request, pk):
        rating = Rating.objects.filter(id=pk, reviewer=request.user).last()
        if not rating:
            return Response({
                "data": {},
                "response_code": status.HTTP_204_NO_CONTENT,
                "response_message": "no content"
            }, status=status.HTTP_204_NO_CONTENT)

        payload = request.data
        rating = Rating.objects.filter(movie=rating.movie).last()
        if payload["rating"] < 1 or payload["rating"] > 5:
            return Response({
                "data": {},
                "response_code": status.HTTP_409_CONFLICT,
                "response_message": "rating out of range"
            }, status=status)

        rating.score = payload["rating"]
        rating.save()
        # get total rating of this movie
        total_rating_count = Rating.objects.filter(movie=rating.movie).count()
        total_rating = 0
        for rating in Rating.objects.filter(movie=rating.movie):
            total_rating += rating.score

        avg_rating = total_rating / total_rating_count
        movie = Movie.objects.filter(id=rating.movie.id).last()
        movie.avg_rating = avg_rating
        movie.save()
        return Response({
            "data": {},
            "response_code": status.HTTP_200_OK,
            "response_message": "success"
        }, status=status.HTTP_200_OK)


class ReportMovieAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movie = Movie.objects.filter(id=request.query_params.get("movie_id")).last()
        if not movie:
            return Response({
                "data": {},
                "response_code": status.HTTP_204_NO_CONTENT,
                "response_message": "no content"
            }, status=status.HTTP_204_NO_CONTENT)

        report_movie = ReportMovie(movie=movie, created_by=request.user,
                                   report="unresolved")
        report_movie.save()
        return Response({
            "data": {},
            "response_code": status.HTTP_200_OK,
            "response_message": "movie reported"
        }, status=status.HTTP_200_OK)


class ReportedMoviesListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportMovieSerializer

    def get(self, request):
        if request.user.is_superuser:
            reported_movies = ReportMovie.objects.all()
            reported_movies_serializer = self.serializer_class(reported_movies, many=True)
            return Response({
                "data": reported_movies_serializer.data,
                "response_code": status.HTTP_200_OK,
                "response_message": "success"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "data": {},
                "response_code": status.HTTP_401_UNAUTHORIZED,
                "response_message": "you're not authorized!"
            }, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_superuser:
            rating_id = request.query_params.get("rating_id")
            rating = Rating.objects.filter(id=rating_id).last()
            movie = Movie.objects.filter(id=rating.movie.id).last()
            payload = request.data
            if "inappropriate" in payload["state"]:
                rating.state = "make movie as inappropriate"
                movie.state = "make movie as inappropriate"
                movie.save()

            if "reject report" in payload["state"]:
                movie.state = "reject report"
                movie.state = ""
                movie.save()

            return Response({
                "data": {},
                "response_message": "report action complete",
                "response_code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "data": {},
                "response_message": "you're not authorized",
                "response_code": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)