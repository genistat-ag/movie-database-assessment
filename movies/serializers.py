from rest_framework import serializers
from .models import Movie,Rating,Report,STATE_CHOICES
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='username')
    avg_rating = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genre', 'year', 'creator', 'avg_rating')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'movies')


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False,queryset=Movie.objects.all())
    reviewer = serializers.ReadOnlyField(source='username')
    score=serializers.IntegerField()

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
    
class ReportSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(many=False, queryset=Movie.objects.all())
    reporter = serializers.ReadOnlyField(source='username')
    state = serializers.ChoiceField(choices=STATE_CHOICES, required=False)

    # Info: Here Using the Finite State Pattern to Change the Report Type
    def update(self, instance, validated_data):
        if self.context['request'].user.is_superuser:
            _state = validated_data.get('state', instance.state)
            if _state == "mark_as_inappropriate":
                instance.to_state_mark_as_inappropriate()
            if _state == "reject_report":
                instance.to_state_reject_report()
            if _state == "unresolved":
                instance.to_state_unresolved()
            instance.save()
        else:
            raise serializers.ValidationError('Only superadmins can change the state of a report.')
        return instance
    
    class Meta:
        model = Report
        fields = ('id', 'movie', 'state', 'reporter')