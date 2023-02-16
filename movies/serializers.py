from rest_framework import serializers

from .constants import INAPPROPRIATE
from .models import Movie, Rating, Report
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating')


class OwnMovieSerializer(MovieSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update({'is_inappropriate': instance.reports.filter(movie=instance).exists()})
        return data


class ReportSerializer(serializers.ModelSerializer):  # create class to serializer model
    user = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Report
        fields = ('id', 'state', 'user', 'movie', 'description')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Rating
        fields = ('id','movie','score','reviewer')