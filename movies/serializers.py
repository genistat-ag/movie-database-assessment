from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie,Rating, Report

class UserSerializer(serializers.ModelSerializer):
    """User Serializer For Movies"""
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')

class MovieSerializer(serializers.ModelSerializer):
    """
    Responsible for serializing Movies.
    Returns:
       OrderDict: Serialized Movie
   """
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator',)

    def to_representation(self, instance):
        """
        Decorating Movie object with rating and inappropriate fields
        """
        result = super().to_representation(instance)
        if instance.avg_rating and instance.avg_rating > 0:
            result['rating'] = f'{instance.avg_rating:.2f}'
        if not instance.is_active:
            result['inappropriate'] = 1
        return result

class RatingSerializer(serializers.ModelSerializer):
    """
    Reposnisble for Serializing Reviews.
    Raises:
        serializers.ValidationError: If value is less than 1 OR greater than 5, serializer will raise validation error.
    Returns:
        OrderDict: Serialized Review Object.
    """
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
    """
     Reponsible for Serializing Reports

     Returns:
         OrderDict: Serialized Review Object.
    """
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='reporter.username')

    def create(self, validated_data):
        reporting_user = validated_data.get("reporter")
        reporting_movie = validated_data.get('movie')
        if Report.objects.filter(movie=reporting_movie, reporter=reporting_user, is_closed=False).exists():
            raise serializers.ValidationError({"error":"Your have already submitted a report for this movie."})

        return super().create(validated_data)

    class Meta:
        model = Report
        fields = ('id','movie','report_state','reporter')