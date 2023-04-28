from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Rating, Movie


@receiver(post_save, sender=Rating, dispatch_uid="update_rating")
def update_avg_rating(sender, instance, **kwargs):
    """
    Updates the average rating of the movie after a new rating is added
    """
    movie = instance.movie
    ratings = Rating.objects.filter(movie=movie)
    avg_rating = sum(rating.score for rating in ratings) / len(ratings)
    movie.avg_rating = avg_rating
    movie.save(update_fields=['avg_rating'])
