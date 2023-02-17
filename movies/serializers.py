from rest_framework import serializers
from .models import Movie, Rating, Report
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')
    # avg_rating = serializers.ReadOnlyField()
    creator_detail = serializers.SerializerMethodField(read_only=True)
    avg_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'genre',
            'year',
            'creator',
            'creator_detail',
            'avg_rating',
            'created_at',
            'updated_at',
        ]

    def get_creator_detail(self, obj):
        if obj.creator:
            return {
                'id': obj.creator.id,
                'username': obj.creator.username,
                'email': obj.creator.email,
            }
        return None
    def get_avg_rating(self, obj):
        a='bfg'
        if obj:
            return obj.avg_rating
        return None


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')
    movie_details = serializers.SerializerMethodField(read_only=True)
    reviewer_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        fields = (
            'id',
            'score',
            'reviewer',
            'reviewer_details',
            'movie',
            'movie_details',
            'created_at',
            'updated_at',
        )

    def get_movie_details(self, obj):
        if obj.movie:
            serializer = MovieSerializer(instance=obj.movie)
            return serializer.data
        return None

    def get_reviewer_details(self, obj):
        if obj.reviewer:
            context = {
                'id':obj.reviewer.id,
                'username':obj.reviewer.username,
                'email':obj.reviewer.email,
            }
            return context
        return None


class ReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='username')
    movie_details = serializers.SerializerMethodField(read_only=True)
    reporter_details = serializers.SerializerMethodField(read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Report
        fields = (
            'id',
            'status',
            'reporter',
            'reporter_details',
            'movie',
            'movie_details',
            'created_at',
            'updated_at',
        )

    def get_movie_details(self, obj):
        if obj.movie:
            serializer = MovieSerializer(instance=obj.movie)
            return serializer.data
        return None

    def get_reporter_details(self, obj):
        if obj.reporter:
            context = {
                'id':obj.reporter.id,
                'username':obj.reporter.username,
                'email':obj.reporter.email,
            }
            return context
        return None


class ReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'status',
        )