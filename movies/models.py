from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=255,unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True,blank=True)
    is_inappropriate = models.BooleanField(default=False)

    def save(self, update_fields=[]):
        if 'avg_rating' not in update_fields:
            self.updated_at = timezone.now()
        return super().save()

    class Meta:
        ordering = ['-id']


class Rating(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Report(models.Model):
    STATE_UNRESOLVED = 0
    STATE_INAPPROPRIATE = 1
    STATE_REJECT = 2
    STATUS_CHOICES = (
        (STATE_UNRESOLVED, 'unresolved'),
        (STATE_INAPPROPRIATE, 'inappropriate'),
        (STATE_REJECT, 'close'),
    )
    movie = models.ForeignKey(Movie,related_name='marked',on_delete=models.CASCADE)
    reporter= models.ForeignKey('auth.User', related_name='reporter', on_delete=models.CASCADE)
    state = models.IntegerField(choices=STATUS_CHOICES, default=STATE_UNRESOLVED)
