from rest_framework import serializers
from .models import Movie, Rating, Report
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


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.ReadOnlyField(source='username')
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())

    class Meta:
        model = Report
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('state', None)
        validated_data.pop('is_closed', None)
        
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('created_at', None)

        if validated_data.get('state') == Report.REJECTED: #Delete report if report set as rejected
            instance.delete()
        else:
            super().update(instance, validated_data)
        
        return instance