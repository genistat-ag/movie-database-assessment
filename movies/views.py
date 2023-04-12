from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from .models import Movie,Rating,Report
from .serializers import MovieSerializer,ReviewSerializer,ReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwnerOrReadOnly, IsRatingOwnerOrReadOnly  # adding pre-built custom permission
from django.db.models import Q
from django.db.models import Subquery, OuterRef
from django.core.exceptions import ValidationError
# Removes permissions from views


"""
@create_by jibon


It's a module level private function. To keep my code DRY 
i thought of creating this method. As stated in Use case
`When a movie review is created/updated the avg_rating field of the specific movie should get updated automatically.`
Its a specific feature add method not a bug fix
"""
def _calculate_movie_avg_ratings(instance: Rating):
    movie = instance.movie
    ratings = Rating.objects.filter(movie=movie)
    avg_rating = sum([rating.score for rating in ratings]) / len(ratings)
    movie.avg_rating = avg_rating
    # This will not update movie updated_at field as update_fields is fixed
    movie.save(update_fields=['avg_rating'])


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)


    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        user = self.request.user

        # check for any `mark_as_inappropriate movies marked by user`
        inappropriate_movies = Movie.objects.annotate(
            has_marked_reports=Subquery(
                Report.objects.filter(
                    movie_id=OuterRef('pk'),
                    state='mark_as_inappropriate',
                    reporter_id=user.id
                ).values('movie_id')
            )
        ).filter(has_marked_reports=True)

        reject_movies = Movie.objects.annotate(
                            has_report_closed=Subquery(
                                Report.objects.filter(
                                    movie_id=OuterRef('pk'),
                                    state='reject_report',
                                ).values('movie_id')
                            )
                        ).filter(has_report_closed=True)

        # get all the movies with is_hidden=False
        movies = Movie.objects.filter(is_hidden=False)

        if inappropriate_movies.exists():
            # combilne the inappropriate_movies with queryset as these are created by this user
            queryset = movies | inappropriate_movies | reject_movies
        else:
            queryset = movies | reject_movies
        return queryset
            


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    """
    Bug Fix: 
    =================================
    Permission Was not added in this view.
    Here applying the clause `A movie can only be updated by its creator`
    With the help of pre-created `IsOwnerOrReadOnly` permission.
    Also `All movies created by users are accessible for viewing by any authenticated user`
    clause is resolved with `IsAuthenticated` permission
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    # Handling the update and permissions will be checked 
    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)

    # Handling the delete and permissions will be checked
    def perform_destroy(self, instance):
        instance.delete()



class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        instance = serializer.save(reviewer=self.request.user)
        # Update the average rating of the movie
        _calculate_movie_avg_ratings(instance)


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    """
        As stated in use case `A user can change their rating more than once. But only their own ratings.`
        A custom permission `IsRatingOwnerOrReadOnly` is made. This will handle the permission if 
        a user is logged in & the update review does belongs to the user
    """
    permission_classes = [IsAuthenticated, IsRatingOwnerOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        # Update the average rating of the movie
        _calculate_movie_avg_ratings(instance)

    # Handling the delete and permissions will be checked
    def perform_destroy(self, instance):
        instance.delete()

class ListCreateReportAPIView(ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET' and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to access this resource.", code=401)
        return Report.objects.all() 

    def perform_create(self, serializer):
        # Get the movie associated with the report
        movie = serializer.validated_data.get('movie')
        # Check if the movie's report is closed
        if not movie.is_report_closed:
            # Assign the user who created the report
            instance = serializer.save(reporter=self.request.user)
            return instance
        else:
            raise ValidationError("Reporting is closed for this movie!", code=400)


class RetrieveUpdateDestroyReportAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_update(self, serializer):
        instance = serializer.save()

    # Handling the delete and permissions will be checked
    def perform_destroy(self, instance):
        instance.delete()