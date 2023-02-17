from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='films', on_delete=models.CASCADE)
    avg_rating = models.FloatField(null=True, blank=True)
    is_inappropriate = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']


class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('auth.User', related_name='reviewer', on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class State(models.TextChoices):
    UNRESOLVED = 'unresolved', 'Unresolved'
    MARK_AS_INAPPROPRIATE = 'mark-as-inappropriate', 'Mark as inappropriate'
    REJECT_REPORT = 'reject-report', 'Reject report'
    RESOLVED = 'resolved', 'Resolved'


class Report(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    reporter = models.ForeignKey('auth.User', related_name="reporter", on_delete=models.CASCADE)
    state = models.CharField(max_length=100, choices=State.choices, default=State.UNRESOLVED)

    def mark_as_inappropriate(self):
        self.movie.is_inappropriate = True
        self.movie.save()
        self.state = State.MARK_AS_INAPPROPRIATE
        self.save()

    def reject_report(self):
        self.state = State.REJECT_REPORT
        self.save()

    def revert(self):
        self.state = State.UNRESOLVED
        self.movie.is_inappropriate = False
        self.movie.save()
        self.save()

    def set_state(self, new_state):
        if new_state == State.MARK_AS_INAPPROPRIATE:
            self.mark_as_inappropriate()
        elif new_state == State.REJECT_REPORT:
            self.reject_report()
        elif new_state == State.UNRESOLVED:
            self.revert()
        else:
            raise ValueError('Invalid state transition')
