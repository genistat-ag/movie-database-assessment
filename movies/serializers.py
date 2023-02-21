from rest_framework import serializers
from .models import Movie, Rating, Report
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator')
        read_only_fields = ('created_at', 'updated_at')

    def update(self, instance, validated_data):
        # Don't update created_at during updates
        validated_data.pop('created_at', None)
        return super().update(instance, validated_data)


class MovieDetailSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.StringRelatedField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    # movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    # reviewer = serializers.ReadOnlyField(source='username')
    reviewer = serializers.StringRelatedField(read_only=True)
    movie = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'movie', 'score', 'reviewer')


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.StringRelatedField(read_only=True)
    movie = serializers.StringRelatedField(read_only=True)
    state = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = ('id', 'movie', 'state', 'reporter')

    def update(self, instance, validated_data):
        # Don't update created_at during updates
        validated_data.pop('created_at', None)
        return super().update(instance, validated_data)


class ReportDetailSerializer(serializers.ModelSerializer):
    reporter = serializers.StringRelatedField(read_only=True)
    movie = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
