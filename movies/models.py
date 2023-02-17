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

    def __str__(self):
        if self.title:
            return 'The Movie is = ' + \
                str(self.title) + ', And the Average Rating is = ' + str(self.avg_rating)

        return str(self.id)


class Rating(models.Model):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.movie:
            return 'The Movie is '+\
                str(self.movie.title)+ ' And the Average Rating is '+str(self.movie.avg_rating)

        return str(self.id)


class Report(models.Model):
    STATUS = [
        ("UNRESOLVED", "Unresolved"),
        ("INAPPROPRIATE", "Inappropriate"),
        ("REJECT", "Reject")
    ]
    movie = models.ForeignKey(Movie, related_name='reports',
                              on_delete=models.CASCADE)
    reporter = models.ForeignKey('auth.User',
                                 related_name='reports',
                                 on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS,
                              default='UNRESOLVED',
                              max_length=50)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.movie:
            return self.movie.title
        return str(self.id)
