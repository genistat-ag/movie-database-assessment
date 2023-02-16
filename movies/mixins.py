from .models import Movie, Rating, Report
from .serializers import MovieSerializer, ReviewSerializer, ReportSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class MovieMixin:
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated,)


class ReportMixin:
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAdminUser,)


class RatingMixin:
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)