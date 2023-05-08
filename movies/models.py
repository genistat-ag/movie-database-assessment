from django.db import models
from django_fsm import FSMField, transition

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Movie(BaseModel):
    title = models.CharField(max_length=255,unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
    
    @property
    def avg_rating(self):
        rating = self.movie.aggregate(models.Avg('score'))
        return rating['score__avg']
    
    @property
    def status(self):
        report = self.report.filter(status='inappropriate').first()
        if report:
            return report.status
        return None


class Rating(BaseModel):
    movie = models.ForeignKey(Movie,related_name='movie',on_delete=models.CASCADE)
    creator = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()


class Report(BaseModel):
    choices = (
        ('unresolved', 'unresolved'),
        ('inappropriate', 'inappropriate'),
        ('reject', 'Reject')
    )
    movie = models.ForeignKey(Movie, related_name='report', on_delete=models.CASCADE)
    reporter = models.ForeignKey('auth.User', related_name='reporter', on_delete=models.CASCADE)
    status = FSMField(choices=choices, default='unresolved', protected=True)

    @transition(field=status, source='unresolved', target='inappropriate')
    def approve(self):
        return f"{self.movie.title} mark as inappropriate"
    
    @transition(field=status, source='unresolved', target='reject')
    def reject(self):
        return 'Report rejected'

    @transition(field=status, source='inappropriate', target='reject')
    def approveToReject(self):
        return 'Report status inappropriate to rejected'

    @transition(field=status, source='reject', target='inappropriate')
    def rejectToApprove(self):
        return 'Report status rejected to inappropriate'
