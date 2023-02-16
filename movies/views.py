from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, get_object_or_404, UpdateAPIView, \
    DestroyAPIView, CreateAPIView, ListAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated
from movies import mixins


class ListCreateMovieAPIView(ListCreateAPIView, mixins.MovieMixin):
    """ Here, authenticated users can see all movies for get request"""
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView, mixins.MovieMixin):

    def get_object(self):
        """ A movie can only be updated by its creator. """
        if self.request.method in ['PUT', 'PATCH']:
            return get_object_or_404(Movie, creator=self.request.user, id=self.kwargs.get("pk"))
        return super().get_object()


class ReportCreateAPIView(CreateAPIView, mixins.ReportMixin):
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Assign the user who created the report
        serializer.save(user=self.request.user)


class ReportListAPIView(ListAPIView, mixins.ReportMixin):
    pass


class ReportUpdateAPIView(UpdateAPIView, mixins.ReportMixin):
    pass


class ListCreateReviewAPIView(ListCreateAPIView, mixins.RatingMixin):
    """ Only authenticated users can give ratings. """

    def perform_create(self, serializer):
        """ Don't create more than one ratting for a single movie by same user"""
        rating = Rating.objects.filter(reviewer=self.request.user, movie_id=self.request.data.get('movie'))
        if rating.exists():
            rating.update(score=self.request.data.get('score'))
        else:
            serializer.save(reviewer=self.request.user)


class ReviewUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView, mixins.RatingMixin):

    def get_object(self):
        """ A user can change their rating more than once. But only their own ratings. """
        return get_object_or_404(Rating, reviewer=self.request.user, id=self.kwargs.get("pk"))
