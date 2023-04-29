from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Movie, Rating


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    # bug: no field named username in Movie model
    # must be mapped to username attribute from creator field
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Movie
        fields = ("id", "title", "genre", "year", "creator", "avg_rating", "status")  # include avg_rating and status
        read_only_fields = ["avg_rating", "status"]  # avg_rating and status are not movie table fields, so read-only


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ("id", "username", "movies")


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    # bug: no field named username in Rating model
    # must be mapped to username attribute from creator field
    reviewer = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Rating
        fields = ("id", "movie", "score", "reviewer")

    # bug: no method available previously to create a new review
    def create(self, validated_data):
        author = self.context["request"].user
        if Rating.objects.filter(movie=validated_data["movie"], creator=author).exists():
            raise serializers.ValidationError({"error": "You already reviewed this movie"})
        return super().create(validated_data)
