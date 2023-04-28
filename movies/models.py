from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


class ReportStatusChoice(models.TextChoices):
    UNRESOLVED = ('unresolved', 'Unresolved')
    INAPPROPRIATE = ('inappropriate', 'Mark movie as inappropriate')
    REJECT = ('reject', 'Reject report')


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        'auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-id']


class Rating(models.Model):
    movie = models.ForeignKey(
        Movie, related_name='movie', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        'auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'reviewer')


class Report(models.Model):
    movie = models.ForeignKey(
        Movie, related_name='reports', on_delete=models.CASCADE)
    reporter = models.ForeignKey(
        'auth.User', related_name='reports', on_delete=models.CASCADE)
    state = models.CharField(
        max_length=255, choices=ReportStatusChoice.choices, default=ReportStatusChoice.UNRESOLVED)
    is_closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.state == ReportStatusChoice.REJECT:
            self.is_closed = True
        return super().save(*args, **kwargs)


@receiver(post_save, sender=Rating)
def update_avg_movie_rating(sender, instance, created, **kwargs):
    Movie.objects.filter(
        id=instance.movie.id
    ).update(avg_rating=instance.movie.movie.aggregate(models.Avg('score'))[
        'score__avg'])
