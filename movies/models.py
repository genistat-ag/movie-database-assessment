from django.db import models


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Movie(BaseTimeModel):
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    @property
    def avg_rating(self):
        rating = self.movie.aggregate(models.Avg('score'))
        return rating['score__avg']

    @property
    def status(self):
        report = self.report.filter(status='inappropriate').first()
        if report:
            return report.status
        return None


class Rating(BaseTimeModel):
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE)
    creator = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()


class Report(BaseTimeModel):
    STATE_CHOICES = (
        ('unresolved', 'unresolved'),
        ('inappropriate', 'Mark movie as inappropriate'),
        ('reject', 'Reject Report')
    )
    movie = models.ForeignKey(Movie, related_name='report', on_delete=models.CASCADE)
    reporter = models.ForeignKey('auth.User', related_name='reporter', on_delete=models.CASCADE)
    status = models.CharField(max_length=14, choices=STATE_CHOICES, default='Unresolved')



