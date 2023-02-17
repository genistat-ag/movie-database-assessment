from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Movie,Rating, Report
from .utils import ChoicesField


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User Serializer For Movies"""
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class MovieSerializer(serializers.ModelSerializer):
    """Movie's Serializer"""
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator',)
    
    def to_representation(self, instance):
        result = super().to_representation(instance)
        if not instance.is_active:
            result['inappropriate'] = 1
        return result


class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer"""
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='reviewer.username')

    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Value must be between 1 to 5")
        return super().validate(value)

    class Meta:
        model = Rating
        fields = ('id','movie','score','reviewer')


class ReportSerializer(serializers.ModelSerializer):
    """ Report Serializer"""
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='reporter.username')
    report_state = ChoicesField(Report.Status.choices)

    class Meta:
        model = Report
        fields = ('id','movie','report_state','reporter')
