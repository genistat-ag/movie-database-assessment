from django.db import models


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
