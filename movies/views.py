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
    """
    <div style='text-align: justify;'>
        This API is used to create or view movies. it is only for authenticated users.
        authenticated users can see all movies but can't modify it. he/she only able to modify his/her own movies.
        <ul>
        <li> It performs create operation after sending a post request </li>
        <li> It gives a list of movie after sending a get request.</li>
        </ul>
    </div>
    """

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
    """
    <div style='text-align: justify;'>
        This API is used to see own movie list. only authenticated users can see his/her own movies
        <ul>
            <li> It gives a list of own movie after sending a get request.</li>
        </ul>
    </div>
    """

    serializer_class = OwnMovieSerializer

    def get_queryset(self):
        return Movie.objects.filter(creator=self.request.user)


class RetrieveUpdateDestroyMovieAPIView(mixins.MovieMixin, RetrieveUpdateDestroyAPIView):
    """
    <div style='text-align: justify;'>
        This API is used to get Three HTTP methods functionality like put, patch, and delete for movie.
        it is only for authenticated users and non-authenticated users can't access it. A movie can only be updated by
        its creator. but all movies created by users are accessible for viewing by any authenticated user.
        <ul>
            <li> It performs an update operation after sending a put request.</li>
            <li> It performs a partial update operation after sending a patch request.</li>
            <li> It performs a delete operation after sending a delete request.</li>
        </ul>
    </div>
    """

    def get_object(self):
        """ A movie can only be updated by its creator. """
        if self.request.method in ['PUT', 'PATCH']:
            return get_object_or_404(Movie, creator=self.request.user, id=self.kwargs.get("pk"))
        return super().get_object()


class ReportCreateAPIView(mixins.ReportMixin, CreateAPIView):
    """
    <div style='text-align: justify;'>
        This API is used to create report. it's only open for authenticated users.
        <ul>
             <li> It performs create operation after sending a post request </li>
        </ul>
    </div>
    """

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Assign the user who created the report
        serializer.save(user=self.request.user)


class ReportListAPIView(mixins.ReportMixin, ListAPIView):
    """
    <div style='text-align: justify;'>
        This API is used to update report. it's only open for authenticated admin users.
        <ul>
            <li> It gives a list of report after sending a get request.</li>
        </ul>
    </div>
    """
    pass


class ReportUpdateAPIView(mixins.ReportMixin, UpdateAPIView):
    """
    <div style='text-align: justify;'>
        This API is used to update report. it's only open for authenticated admin users.
        <ul>
            <li> It performs an update operation after sending a put request.</li>
            <li> It performs a partial update operation after sending a patch request.</li>
        </ul>
    </div>
    """
    pass


class ListCreateReviewAPIView(mixins.RatingMixin, ListCreateAPIView):
    """
    <div style='text-align: justify;'>
        This API is used to create or view ratting list. it is only for authenticated users.
        <ul>
        <li> It performs create operation after sending a post request </li>
        <li> It gives a list of ratting after sending a get request.</li>
        </ul>
    </div>
    """

    def perform_create(self, serializer):
        """ Don't create more than one ratting for a single movie by same user"""
        rating = Rating.objects.filter(reviewer=self.request.user, movie_id=self.request.data.get('movie'))
        if rating.exists():
            rating.update(score=self.request.data.get('score'))
        else:
            serializer.save(reviewer=self.request.user)


class ReviewUpdateDestroyAPIView(mixins.RatingMixin, UpdateAPIView, DestroyAPIView):
    """
    <div style='text-align: justify;'>
        This API is used to get Three HTTP methods functionality like put, patch, and delete for ratting.
        it is only for authenticated users and non-authenticated users can't access it.
        <ul>
            <li> It performs an update operation after sending a put request.</li>
            <li> It performs a partial update operation after sending a patch request.</li>
            <li> It performs a delete operation after sending a delete request.</li>
        </ul>
    </div>
    """

    def get_object(self):
        """ A user can change their rating more than once. But only their own ratings. """
        return get_object_or_404(Rating, reviewer=self.request.user, id=self.kwargs.get("pk"))
