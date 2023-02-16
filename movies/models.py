from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class Movie(models.Model):
    title = models.CharField(max_length=255,unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-id']


class Report(models.Model):

    STATE_CHOICES = (
        (1, "Unresolved"),
        (2, "Mark movie as inappropriate"),
        (3, "Reject report"),
    )

    movie = models.ForeignKey(Movie,related_name='reports', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='reports', on_delete=models.CASCADE)
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, default=1)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rating(models.Model):
    """ A user can give a rating 1 to 5 for any specific movie """

    RATTING_CHOICES = (
        (1, "ONE"),
        (2, "TWO"),
        (3, "THREE"),
        (4, "FOUR"),
        (5, "FIVE"),
    )

    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField(choices=RATTING_CHOICES)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


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

