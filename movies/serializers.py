from django.db.models import Avg
from rest_framework import serializers
from .models import Movie, Rating, Report
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'is_inappropriate')


class MovieDetailsSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating', 'is_inappropriate')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')
    score = serializers.IntegerField(min_value=1, max_value=5)

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if Rating.objects.filter(movie=validated_data.get('movie'), reviewer=user).exists():
            raise serializers.ValidationError({"detail": "You have already created rating for this movie"})
        rating = Rating.objects.create(**validated_data)
        movie = rating.movie
        score_avg = Rating.objects.filter(movie=movie).aggregate(Avg('score'))
        movie.avg_rating = score_avg['score__avg']
        movie.save(update_fields=['avg_rating'])

        return rating

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        movie = instance.movie
        score_avg = Rating.objects.filter(movie=movie).aggregate(Avg('score'))
        movie.avg_rating = score_avg['score__avg']
        movie.save(update_fields=['avg_rating'])
        return instance

    class Meta:
        model = Rating
        fields = ('id', 'movie', 'score', 'reviewer')


class ReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='username')

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if Report.objects.filter(movie=validated_data.get('movie'), reporter=user).exists():
            raise serializers.ValidationError({"detail": "You have already created reported for this movie"})
        report = Report.objects.create(**validated_data)

        return report

    class Meta:
        model = Report
        fields = ['id', 'movie', 'reporter', 'state']
