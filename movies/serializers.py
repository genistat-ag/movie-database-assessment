from rest_framework import serializers
from .models import Movie, Rating, ReportMovie
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.CharField(source="creator.username", read_only=True, required=False)
    class Meta:
        model = Movie
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source="movie.title")
    reviewer = serializers.CharField(source='reviewer.username')

    class Meta:
        model = Rating
        fields = ('id', 'movie', 'score', 'reviewer')

class ReportMovieSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(read_only=True, source="movie.title")
    created_by = serializers.CharField(read_only=True, source="created_by.username")

    class Meta:
        model = ReportMovie
        fields = "__all__"
