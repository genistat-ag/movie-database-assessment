from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255,unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True,blank=True)
    is_active= models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']


class Rating(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Report(models.Model):

    class Status(models.TextChoices):
        UNRESOLVED = 'UNRESOLVED', 'Unresolved'
        REJECTED =  'REJECTED', 'Rejected'
        ACCEPTED = 'ACCEPTED', "Accepted"

    movie = models.ForeignKey(Movie, related_name='reported_movie', on_delete=models.CASCADE)
    report_state = models.CharField(choices=Status.choices, max_length=30, default=Status.UNRESOLVED)
    reporter = models.ForeignKey('auth.User', related_name='reporter', on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)