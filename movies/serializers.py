from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Movie, Rating, Report


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

    # new: no method available previously to create a new review
    def create(self, validated_data):
        author = self.context["request"].user
        if Rating.objects.filter(movie=validated_data["movie"], creator=author).exists():
            raise serializers.ValidationError({"error": "movie already reviewed"})
        return super().create(validated_data)


# new: serializer for retrieving reported movie information
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "movie", "reporter", "status"]
        read_only_fields = ["movie", "reporter"]


# new: serializer for storing reported movie information
class CreateReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source="reporter.username")

    class Meta:
        model = Report
        fields = ["id", "movie", "reporter", "status"]

    def create(self, validated_data):
        author = self.context["request"].user
        if Report.objects.filter(movie=validated_data["movie"], reporter=author).exists():
            raise serializers.ValidationError({"error": "movie already reported"})
        return super().create(validated_data)
