from rest_framework import serializers
from .models import Movie,Rating,Report
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'is_inappropriate')


class MovieRetrieveSerializer(serializers.ModelSerializer):  # create class to serializer model
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
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')
    score = serializers.IntegerField(required=True, max_value=5, min_value=1)

    class Meta:
        model = Rating
        fields = ('id','movie','score','reviewer')


class ReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Report
        fields = ('id','movie','reporter')


class ReportRetrieveSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='username')
    state = serializers.IntegerField(max_value=2, min_value=0)
    state_text = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Report
        fields = ('id','movie','reporter','state')

    def get_state_text(self, ob):
        return ob.get_state_display()