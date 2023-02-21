from datetime import datetime
from django.db.models import Avg

from .models import Movie, Rating, Report


def calculate_movie_review_avg(movie_id):
    """
    Calculate Movie Rating based on previous calculations

    Args:
        movie_id (int): _description_
    """
    avg_rating = Rating.objects.filter(movie_id=movie_id).aggregate(Avg('score'))
    Movie.objects.filter(id=movie_id).update(avg_rating=avg_rating['score__avg'])


def toggle_reported_movie_is_active(report):
    """
    Close the unresolved report once the report is decided.

    Args:
        report (Report): Report object that needs to be decided.

    Close the report and if the report decision is accepted than update all the pending decisions to be accepted for the movie.
    """
    report.is_closed = True
    report.save()

    movie = report.movie
    if report.report_state == Report.Status.ACCEPTED.value:
        Report.objects.filter(movie_id=movie.id, report_state=Report.Status.UNRESOLVED).update(
            is_closed=True,
            report_state=Report.Status.ACCEPTED,
            updated_at=datetime.now()
        )
        movie.is_active = False
    movie.save()