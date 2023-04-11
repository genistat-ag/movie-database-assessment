from rest_framework import serializers
from .models import Movie,Rating,Report,STATE_CHOICES
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')

    class Meta:
        model = Rating
        fields = ('id','movie','score','reviewer')
    
    """
        As stated in clause `A user can give a rating between 1 to 5 for any specific movie`
        It would handle that clause
    """
    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value
    
class ReportSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    state = serializers.ChoiceField(choices=STATE_CHOICES, default="unresolved")
    reporter = serializers.ReadOnlyField(source='username')
    
    class Meta:
        model = Report
        fields = ('id', 'movie', 'state', 'reporter')