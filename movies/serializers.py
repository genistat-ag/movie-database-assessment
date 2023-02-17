from rest_framework import serializers
from .models import Movie,Rating
from django.contrib.auth.models import User

from django.db.models import Avg

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'details', 'creator', 'avg_rating')
    
    def get_avg_rating(self, obj):
        return obj.movie.aggregate(Avg('score')).get('score__avg')


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