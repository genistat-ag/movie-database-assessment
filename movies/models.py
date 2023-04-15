from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255,unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True,blank=True)
    is_inappropriate = models.BooleanField(default=False)


    class Meta:
        ordering = ['-id']

    def update_avg_rating(self):
        """ 
            -  When a movie review is created/updated, the avg_rating field of the  specific movie should get updated automatically.
            -  The updated_at field should not change when updating the avg_rating field (It should only change when a movie is edited).
        """
        reviews = Rating.objects.filter(movie=self)
        if reviews.exists():
            avg_rating = sum(review.score for review in reviews) / len(reviews)
        else:
            avg_rating = None
        if self.avg_rating != avg_rating:
            self.avg_rating = avg_rating
            self.save(update_fields=['avg_rating'])


class Rating(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    creator = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE) #change to use isowner permission class
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) #A user can give a rating between 1 to 5 for any specific movie.
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class MovieReport(models.Model):
    UNRESOLVED = 'unresolved'
    MARKED_INAPPROPRIATE = 'marked_inappropriate'
    REJECTED = 'rejected'
    STATE_CHOICES = (
        (UNRESOLVED, 'Unresolved'),
        (MARKED_INAPPROPRIATE, 'Marked as Inappropriate'),
        (REJECTED, 'Rejected'),
    )
    movie = models.ForeignKey(Movie, related_name='reports', on_delete=models.CASCADE)
    creator = models.ForeignKey('auth.User', related_name='reports_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=UNRESOLVED)

    def mark_as_inappropriate(self):
        self.movie.is_inappropriate = True
        self.movie.save()

    def reject_report(self):
        self.movie.is_inappropriate = False
        self.movie.save()

    def unresolved_report(self):
        self.movie.is_inappropriate = False
        self.movie.save()
