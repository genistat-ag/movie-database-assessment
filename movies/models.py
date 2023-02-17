from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

class Movie(models.Model):
    title = models.CharField(max_length=255,unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    visibility=models.BooleanField(null=True,blank=True,default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    # avg_rating = models.FloatField(null=True,blank=True)
    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            sum += rating.score

        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

    class Meta:
        ordering = ['-id']


class Report(models.Model):
    state_choice = [
        ("unresolved","unresolved"),
        ("Mark movie as inappropriate","Mark movie as inappropriate"),
        ("Reject report","Reject report"),
    ]
    movie = models.ForeignKey(Movie,related_name='report_movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='report_reviewer', on_delete=models.CASCADE)
    report = models.TextField(null=True,blank=True)
    state = models.CharField(null=True,blank=True,max_length=255,choices=state_choice,default="unresolved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Rating(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=2,decimal_places=1,validators=[
        MinValueValidator(1),MaxValueValidator(5)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
