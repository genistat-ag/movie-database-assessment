from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

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


class Rating(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=2,decimal_places=1,validators=[
        MinValueValidator(1),MaxValueValidator(5)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
