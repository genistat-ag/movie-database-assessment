from django.db.models import Avg
from .models import Movie, Rating


def calculate_move_review_avg(movie_id: int):
    avg_rating = Rating.objects.filter(movie_id=movie_id).aggregate(Avg('score'))
    Movie.objects.filter(id=movie_id).update(avg_rating=avg_rating['score__avg'])
