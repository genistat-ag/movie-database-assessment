from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from movies.constants import INAPPROPRIATE, REJECTED, UNRESOLVED, SCORE_ONE, \
    SCORE_TWO, SCORE_FIVE,SCORE_THREE,SCORE_FOUR


class Movie(models.Model):
    """  It's used to store all movie data that will be created from user. """

    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class Report(models.Model):
    """
        It's used to store all report data that will be created from non admin user and
        admin user will be able to review it and can take proper steps again it.
    """

    STATE_CHOICES = (
        (UNRESOLVED, "Unresolved"),
        (INAPPROPRIATE, "Mark movie as inappropriate"),
        (REJECTED, "Reject report"),
    )

    movie = models.ForeignKey(Movie, related_name='reports', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='reports', on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, default=1)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'


class Rating(models.Model):
    """ A user can give a rating 1 to 5 for any specific movie """

    RATTING_SCORE_CHOICES = (
        (SCORE_ONE, "ONE"),
        (SCORE_TWO, "TWO"),
        (SCORE_THREE, "THREE"),
        (SCORE_FOUR, "FOUR"),
        (SCORE_FIVE, "FIVE"),
    )

    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField(choices=RATTING_SCORE_CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


@receiver(post_save, sender=Rating)
def increase_avg_rating(sender, instance, created=False, **kwargs):
    """
      ** When a movie review is created the avg_rating field of the specific movie should get updated automatically.
      ** The updated_at field will not change when update the avg_rating field of movie
    """

    if created:
        instance.movie.avg_rating += 1
        instance.movie.save(update_fields=['avg_rating'])


@receiver(post_delete, sender=Rating)
def decrease_update_avg_rating(sender, instance, **kwargs):
    """
      ** When a movie review is updated the avg_rating field of the specific movie should get updated automatically.
      ** The updated_at field will not change when update the avg_rating field of movie
    """

    instance.movie.avg_rating -= 1
    instance.movie.save(update_fields=['avg_rating'])

