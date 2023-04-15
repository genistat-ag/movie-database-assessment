from rest_framework import serializers
from .models import (
    Movie,
    Rating,
    MovieReport
)
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', "is_inappropriate")

class MovieDetailSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if request.user == instance.creator:
                data['creator'] = instance.creator.username
        return data

class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Rating
        fields = ('id', 'movie', 'score', 'creator')


class MovieReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = MovieReport
        fields = ('id', 'movie', 'state', 'creator')

    def create(self, validated_data):
        author = self.context['request'].user
        if MovieReport.objects.filter(movie=validated_data['movie'], creator=author).exists():
            raise serializers.ValidationError({'message': 'You have already reports on this movie'})
        return super().create(validated_data)
    