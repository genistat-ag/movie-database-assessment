from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Movie,Rating, Report
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')
    score = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        model = Rating
        fields = ('id','movie','score','reviewer')


class ReportSerializer(serializers.ModelSerializer):
    # state = serializers.CharField(source='get_state_display')

    class Meta:
        model = Report
        fields = ('id', 'reporter', 'movie', 'state', 'created_at','updated_at')
        # read_only_fields = ('id', 'reporter', 'movie', 'state', 'created_at', 'updated_at',)