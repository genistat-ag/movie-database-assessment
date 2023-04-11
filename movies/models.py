from django.db import models
from django.utils.translation import gettext_lazy as _


from django_fsm import FSMField, transition

STATE_CHOICES = [
        ('unresolved', 'Unresolved'),
        ('mark_as_inappropriate', 'Mark movie as inappropriate'),
        ('reject_report', 'Reject report'),
    ]

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
    score = models.IntegerField()
    # Bug Fix: auto_now_add should be used as per documentaion as it create timezone.now() on object creation time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Report(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    reporter = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    state = FSMField(choices=STATE_CHOICES, default='unresolved', max_length=40, protected=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @transition(field=state, source=['unresolved', 'mark_as_inappropriate'], target='reject_report')
    def to_state_mark_as_inappropriate(self):
        pass

    @transition(field=state, source=['unresolved', 'reject_report'], target='mark_as_inappropriate')
    def to_state_reject_report(self):
        pass

    @transition(field=state, source=['reject_report','mark_as_inappropriate'], target='unresolved')
    def to_state_unresolved(self):
        pass