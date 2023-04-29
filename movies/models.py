from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_fsm import FSMField, transition


# base model created for reducing code duplication
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # no table is created for this model because abstract is True


class Movie(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255)
    year = models.IntegerField()
    creator = models.ForeignKey("auth.User", related_name="films", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]

    # calculate average rating of movie as property reduces write operation on databases
    @property
    def avg_rating(self):
        rating = self.movie.aggregate(models.Avg("score"))
        return rating["score__avg"]

    # include report status on a movie with response
    @property
    def status(self):
        report = self.report.filter(status="inappropriate").first()
        if report:
            return report.status
        return None


class Rating(BaseModel):
    movie = models.ForeignKey(Movie, related_name="movie", on_delete=models.CASCADE)
    # bug: field name being reviewer affected the permission class
    # which necesitates this field being named as creator
    creator = models.ForeignKey("auth.User", related_name="reviewer", on_delete=models.CASCADE)
    # bug: score field is not validated to be between 1 and 5
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


# new: model for storing reported movie information
class Report(BaseModel):
    choices = (("unresolved", "unresolved"), ("inappropriate", "inappropriate"), ("reject", "Reject"))
    movie = models.ForeignKey(Movie, related_name="report", on_delete=models.CASCADE)
    reporter = models.ForeignKey("auth.User", related_name="reporter", on_delete=models.CASCADE)
    status = FSMField(choices=choices, default="unresolved", protected=True)

    # the decorator is used to update the status of the report
    # report approved, and movie is marked as inappropriate
    @transition(field=status, source="unresolved", target="inappropriate")
    def update_as_approve(self):
        return f"{self.movie.title} marked as inappropriate"

    # the decorator is used to update the status of the report
    # report rejected, and movie status remains as normal
    @transition(field=status, source="unresolved", target="reject")
    def update_as_reject(self):
        return f"Report on {self.movie.title} rejected"

    # the decorator is used to update previously approved report
    # report rejected, and movie status is updated as normal
    @transition(field=status, source="inappropriate", target="reject")
    def update_from_approve_to_reject(self):
        return f"Report status on {self.movie.title} changed from inappropriate to rejected"

    # the decorator is used to update previously rejected report
    # report approved, and movie is marked as inappropriate
    @transition(field=status, source="reject", target="inappropriate")
    def update_from_reject_to_approve(self):
        return f"Report status on {self.movie.title} changed from rejected to inappropriate"
