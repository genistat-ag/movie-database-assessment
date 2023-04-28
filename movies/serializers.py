from rest_framework import serializers
from .models import Movie, Rating, Report
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(
        source='creator.username')  # BUG_FIX: access creator's username from creator parent model/ user model
    avg_rating = serializers.ReadOnlyField()
    state = serializers.SerializerMethodField() # Added movie state field if movie has been reported as inappropriate show as inappropriate

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating', 'state')

    def get_state(self, obj):
        if obj.reports.filter(state='inappropriate').exists():
            return 'inappropriate'
        else:
            return None

    def to_representation(self, instance):
        # if the movie is inappropriate, return the state otherwise remove it from the response
        data = super().to_representation(instance)
        if data.get('state'):
            return data
        data.pop('state')
        return data


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='reviewer.username') # BUG_FIX: access reviewer's username from user model

    class Meta:
        model = Rating
        fields = ('id', 'movie', 'score', 'reviewer')

    def validate(self, attrs):
        """
        validation added to Check that the score is between 1 and 5
        """
        if attrs['score'] < 1 or attrs['score'] > 5:
            raise serializers.ValidationError("Score must be between 1 and 5")
        return attrs


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username')
    class Meta:
        model = Report
        fields = ('id', 'movie', 'user', 'state')
        read_only_fields = ('movie', 'user')

    def validate_state(self, value):
        """
        Only SuperAdmins can set the state to "inappropriate" or "reject_report"
        """
        user = self.context['request'].user
        if user.is_superuser or value not in ['inappropriate', 'reject_report']:
            return value
        else:
            raise serializers.ValidationError("Only SuperAdmins can mark a movie as inappropriate or reject a report")
