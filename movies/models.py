from django.db import models
from django_fsm import FSMField, transition

class Movie(models.Model):
    hidden = models.BooleanField(default=False)
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
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class Report(models.Model):
    REPORT_STATES = (
        ('unresolved', 'Unresolved'),
        ('inappropriate', 'Inappropriate'),
        ('rejected', 'Rejected')
    )

    reporter = models.ForeignKey('auth.User', related_name='reporter', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,related_name='movie_report', on_delete=models.CASCADE)
    state = FSMField(default='unresolved', choices=REPORT_STATES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @transition(field=state, source='unresolved', target='inappropriate')
    def mark_inappropriate(self):
        self.movie.hidden = True
        self.movie.save()

    @transition(field=state, source='inappropriate', target='rejected')
    def reject_report(self):
        pass

    @transition(field=state, source='inappropriate', target='unresolved')
    def unmark_inappropriate(self):
        self.movie.hidden = False
        self.movie.save()

    @transition(field=state, source=['unresolved', 'inappropriate'], target='rejected')
    def reject_report_anyway(self):
        pass

