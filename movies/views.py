from django.db.models import Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, get_object_or_404, UpdateAPIView, \
    DestroyAPIView, CreateAPIView, ListAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated
from movies import mixins
from movies.constants import INAPPROPRIATE
from .serializers import OwnMovieSerializer


class ListCreateMovieAPIView(mixins.MovieMixin, ListCreateAPIView):
    """ Here, authenticated users can see all movies for get request"""

    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        """ inappropriate movie will be hidden from all users of the system"""
        return Movie.objects.filter(~Q(reports__state=INAPPROPRIATE))

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class OwnMovieListView(mixins.MovieMixin, ListAPIView):
    """ Here, only authenticated users can see his/her own movies"""

    serializer_class = OwnMovieSerializer

    def get_queryset(self):
        return Movie.objects.filter(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(mixins.MovieMixin, RetrieveUpdateDestroyAPIView):

    def get_object(self):
        """ A movie can only be updated by its creator. """
        if self.request.method in ['PUT', 'PATCH']:
            return get_object_or_404(Movie, creator=self.request.user, id=self.kwargs.get("pk"))
        return super().get_object()


class ReportCreateAPIView(mixins.ReportMixin, CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Assign the user who created the report
        serializer.save(user=self.request.user)


class ReportListAPIView(mixins.ReportMixin, ListAPIView):
    pass


class ReportUpdateAPIView(mixins.ReportMixin, UpdateAPIView):
    pass


class ListCreateReviewAPIView(mixins.RatingMixin, ListCreateAPIView):
    """ Only authenticated users can give ratings. """

    def perform_create(self, serializer):
        """ Don't create more than one ratting for a single movie by same user"""
        rating = Rating.objects.filter(reviewer=self.request.user, movie_id=self.request.data.get('movie'))
        if rating.exists():
            rating.update(score=self.request.data.get('score'))
        else:
            serializer.save(reviewer=self.request.user)


class ReviewUpdateDestroyAPIView(mixins.RatingMixin, UpdateAPIView, DestroyAPIView):

    def get_object(self):
        """ A user can change their rating more than once. But only their own ratings. """
        return get_object_or_404(Rating, reviewer=self.request.user, id=self.kwargs.get("pk"))
