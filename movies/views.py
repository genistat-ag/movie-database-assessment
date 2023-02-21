from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)

from .utils import calculate_movie_review_avg, toggle_reported_movie_is_active
from .models import Movie, Rating, Report
from .serializers import MovieSerializer, ReviewSerializer, ReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from .permissions import (
    IsOwnerOrReadOnly,
    IsReviewerOrReadOnly,
    IsSuperuser,
    IsSuperuserOrAuthenticatedForGetAndPost
)

class ListCreateMovieAPIView(ListCreateAPIView):
    """
    Movie's List and Create API view:
    Create Move (POST):
    - id (System): System generated id,
    - title (required): Movie Title
    - genre (required): Movie Genere
    - year (required): Movie released year
    - creator (System): Creater of the move. (Handled by the system)
    List of Movies (GET):
    - All active movies will be shown.
    - If the authenticated user is the owner of an inactive move than they will see inactive moves with a filed named inappropriate
    """
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Passing Authenticated users as the creator of the move during create"""
        serializer.save(creator=self.request.user, avg_rating=0)

    def get_queryset(self):
        # Movies that are not user's and are inactive will be excluded. ~Q() Not Equal to
        """ Movies that are not user's and are inactive will be excluded. ~Q() Not Equal to """
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().exclude(~Q(creator_id=self.request.user.id), is_active=False)

class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    """
    Move's Detail, Update and Destroy API view:
    Detail of a Movie (GET):
    - id: System generated id,
    - title: Movie Title
    - genere: Movie Genere
    - year: Movie Releasing Year.
    - creator: Movie creator to the system.
    Update Movie (PATCH) (For specific field(s)):
    - title (required): Movie Title
    - genre (required): Movie Genere
    - year (required): Movie released year
    - creator (System): Creater of the move. (Handled by the system)
    Description:
    - Movies that are in-active will be marked as inappropriate and could only be seen by the creator of the movie while making it hidden from other users.
    """
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

class ListCreateReviewAPIView(ListCreateAPIView):
    """
    Review Create and List API view:
    Review List (GET):
    - id: System generated id,
    - movie: Reviewed Move id,
    - score: Reviewed Score,
    - reviewer: Reviewer
    Create Movie Review (POST):
    - id (System): Auto matically added by the system,
    - movie (Required): Movie primary key that is going to be reviewed,
    - score (Required): Review Score. Must be between 1 to 5,
    - reviewer (System): reviewer of the move. (Handled by the system)

    Description:
    - On Each review submit reviewed movie's avg_rating will be updated.
    """
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Update avg_rating of the reviewed movie"""
        saved_review = serializer.save(reviewer=self.request.user)
        calculate_movie_review_avg(saved_review.movie_id)

class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    """
    Review Detail and Update API view:
    Review List (GET):
    - id: System generated id,
    - movie: Reviewed Move id,
    - score: Reviewed Score,
    - reviewer: Reviewer
    Update Movie Review (PATCH) (For specific field(s)):
    - id (System): Auto matically added by the system,
    - movie (Required): Movie primary key that is going to be reviewed,
    - score (Required): Review Score. Must be between 1 to 5,
    - reviewer (System): reviewer of the move. (Handled by the system)

    Description:
    - On Each review update reviewed movie's avg_rating will be updated.
    """
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated, IsReviewerOrReadOnly)

    def perform_update(self, serializer):
        """Update avg_rating of the reviewed movie"""
        saved_review = serializer.save(reviewer=self.request.user)
        calculate_movie_review_avg(saved_review.movie_id)

class ListCreateReportAPIView(ListCreateAPIView):
    """
        Report Create and List API view:
        Superuser's Report List (GET):
        - id: System generated id
        - movie: Reviewed Move id
        - report_state: Report State
        - reporter: Reporting user
        Report Create (POST):
        - movie: Reviewed Move id

        Description:
        - All reports are created initially as UNRESOLVED report.
        - Report's list loaded in decending order of ID.
        - One user cannot submit multiple report for a movie if a report is unresolved for that movie of that particular user.
     """
    serializer_class = ReportSerializer
    queryset = Report.objects.all().order_by('-id')
    permission_classes = (IsSuperuserOrAuthenticatedForGetAndPost,)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

class RetrieveUpdateDestroyReportAPIView(RetrieveUpdateDestroyAPIView):
    """
    Superuser's Report Update, Detail and Destroy API view:
    Report Detail (GET):
    - id: System generated id
    - movie: Reviewed Move id
    - report_state: Report State
    - reporter: Reporting user
    Report Create (POST):
    - report_state: Report Decision (Accepted Values are: "UNRESOLVED", "REJECTED", "ACCEPTED")

    Description:
    - Once the decision is made, the report will be closed and if the reported is accepted
    than the movie is updated to in-acitve and all the unresolved decisions will be also updated as accepted and closed.
    """
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsSuperuser,)

    def perform_update(self, serializer):
        """
        On Update, toggels the movie object to Active or Inactive.
        """
        reported_object = serializer.save()
        toggle_reported_movie_is_active(reported_object)
