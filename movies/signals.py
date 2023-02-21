from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from movies.models import Rating, Report


@receiver(post_save, sender=Rating)
def update_avg_rating(sender, instance, **kwargs):
    movie = instance.movie
    avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg("score"))
    movie.avg_rating = avg_rating
    movie.save(update_fields=['avg_rating'])
    
@receiver(post_save, sender=Report)
def mark_movie_as_inappropriate(sender, instance, **kwargs):
    movie = instance.movie
    if instance.state == 1:
        movie.is_inappropriate=True
    else:
        movie.is_inappropriate=False
    movie.save()