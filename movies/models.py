from django.db import models


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
    score = models.IntegerField()
