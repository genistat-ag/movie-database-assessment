from collections import OrderedDict
from django.db.models import Avg

from rest_framework import serializers
from .models import Movie, Rating, Report


def calculate_move_review_avg(movie_id: int):
    avg_rating = Rating.objects.filter(movie_id=movie_id).aggregate(Avg('score'))
    Movie.objects.filter(id=movie_id).update(avg_rating=avg_rating['score__avg'])


def toggle_reported_movie_is_active(report: Report):
    movie = report.movie
    print("STATUS", report.report_state)
    if report.report_state == Report.Status.REJECTED.value:
        movie.is_active = True
    elif report.report_state == Report.Status.ACCEPTED.value:
        movie.is_active = False
        print(movie.is_active)

    movie.save()


class ChoicesField(serializers.Field):
    """Custom ChoiceField serializer field."""

    def __init__(self, choices, **kwargs):
        self._choices = dict(choices)
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        for choice in self._choices:
            if choice == data:
                return choice
        raise serializers.ValidationError(f"Acceptable values are {self._choices.keys()}")
