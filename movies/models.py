from django.db import models
from django_fsm import FSMField, transition


class Movie(models.Model):
    title = models.CharField(max_length=255,unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True,blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.title} - {self.genre}'

class Rating(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f'{self.movie.title} - {self.score}'


class Report(models.Model):


    UNRESOLVED = 'UNRESOLVED'
    REJECTED =  'REJECTED'
    INAPPROPRIATE_MOVIE = 'INAPPROPRIATE_MOVIE'

    STATE_CHOICES = (
        (UNRESOLVED, 'Unresolved'),
        (REJECTED, 'Reject Report'),
        (INAPPROPRIATE_MOVIE, 'Mark movie as inappropriate'),
    )

    movie = models.ForeignKey(Movie, related_name='reproted_movie', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    state = FSMField(default=UNRESOLVED, choices=STATE_CHOICES)
    reporter = models.ForeignKey('auth.User', related_name='reporter', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.movie.title}_{self.state}'
