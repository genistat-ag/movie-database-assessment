from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True, blank=True)
    hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']


class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Report(models.Model):
    REPORT_CHOICES = (
        ('unresolved', 'Unresolved'),
        ('inappropriate', 'Mark movie as inappropriate'),
        ('rejected', 'Reject report')
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=REPORT_CHOICES, default='unresolved')
