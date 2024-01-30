from rest_framework import serializers
from .models import Movie, Rating, Report
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating', 'status')
        read_only_fields = ['avg_rating', 'status']


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Rating
        fields = ('id','movie','score','reviewer')
    
    def create(self, validated_data):
        author = self.context['request'].user
        if Rating.objects.filter(movie=validated_data['movie'], creator=author).exists():
            raise serializers.ValidationError({'error': 'You already reviewed this movie'})
        return super().create(validated_data)


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'movie', 'reporter', 'status']
        read_only_fields = ['movie', 'reporter']


class CreateReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = Report
        fields = ['id', 'movie', 'reporter', 'status']

    def create(self, validated_data):
        author = self.context['request'].user
        if Report.objects.filter(movie=validated_data['movie'], reporter=author).exists():
            raise serializers.ValidationError({'error': 'You already reported this movie'})
        return super().create(validated_data)
