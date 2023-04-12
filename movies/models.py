from django.db import models


class MoviesCoreModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Movie(MoviesCoreModel):
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        ordering = ['-id']


class Rating(MoviesCoreModel):
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()


class ReportMovie(MoviesCoreModel):
    STATES = [
        ("unresolved", "unresolved"),
        ("mark movie as inappropriate", "mark movie as inappropriate"),
        ("reject report", "reject report"),
    ]
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    report = models.CharField(choices=STATES, null=True, blank=True, max_length=50)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
