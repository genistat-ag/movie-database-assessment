from rest_framework import serializers
from .models import Movie, Rating
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username') # access creator's username from creator parent model/ user model
    # creator = serializers.ReadOnlyField(source='username')
    avg_rating = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='reviewer.username')

    class Meta:
        model = Rating
        fields = ('id', 'movie', 'score', 'reviewer')

    def validate(self, attrs):
        """
        Check that the score is between 1 and 5
        """
        if attrs['score'] < 1 or attrs['score'] > 5:
            raise serializers.ValidationError("Score must be between 1 and 5")
        return attrs
