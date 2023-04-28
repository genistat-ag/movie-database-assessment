from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Movie, Rating, Report, ReportStatusChoice


# create class to serializer model
class MovieSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating')
        extra_kwargs = {'avg_rating': {'read_only': True}}

# create class to serializer user model


class UserMovieSerializer(MovieSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.reports.filter(
            state=ReportStatusChoice.INAPPROPRIATE
        ).exists():
            data['report_state'] = 'inappropriate'
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['movies'] = UserMovieSerializer(
            instance.films.all(), many=True).data
        return data


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')
    score = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ('id', 'movie', 'score', 'reviewer')

    def create(self, validated_data):
        if Rating.objects.filter(
            movie=validated_data['movie'],
            reviewer=validated_data['reviewer'],
        ).exists():
            raise serializers.ValidationError(
                'You have already reviewed this movie')

        return super().create(validated_data)

    # def create(self, validated_data):
    #     rating, created = Rating.objects.get_or_create(
    #         movie=validated_data['movie'],
    #         reviewer=validated_data['reviewer'],
    #     )
    #     rating.score = validated_data.get('score', rating.score)
    #     rating.save()
    #     return rating


class ReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Report
        fields = (
            'id',
            'movie',
            'reporter',
            'state',
            'is_closed',
        )
