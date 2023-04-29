from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .filters import MovieFilter
from .models import Movie, Rating, Report
from .pagination import CustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CreateReportSerializer,
    MovieSerializer,
    ReportSerializer,
    ReviewSerializer,
)


class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)

    # new: filtering not done for inappropriate movies when user is not creator
    def get_queryset(self):
        query = super().get_queryset()
        ids = []
        for i in query:
            if i.status == "inappropriate":
                if i.creator == self.request.user:
                    ids.append(i.id)
            else:
                ids.append(i.id)
        return query.filter(id__in=ids)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)  # bug: only owner can update or delete movie
    http_method_names = ["get", "put", "delete"]  # restrict available methods


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # update: reivewer -> creator for field name as modified in model
        serializer.save(creator=self.request.user)


# new: endpoints to read or update reviews
class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ["get", "put", "delete"]


# new: endpoints to create or list reported movies
class ListCreateReportAPIView(ListCreateAPIView):
    serializer_class = CreateReportSerializer
    queryset = Report.objects.all()

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


# new: endpoint to update reported movies
class ReportReview(UpdateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAdminUser]
    http_method_names = ["put"]


# new: endpoints to approve reported movie to mark as inappropriate
class ApproveReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.update_as_approve()
            obj.save()
            return Response(self.get_serializer(obj).data)
        except Exception:
            return Response("report previously resolved")


# new: endpoints to reject reported movie to remain as appropriate
class RejectReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.update_as_reject()
            obj.save()
            return Response(self.get_serializer(obj).data)
        except Exception:
            return Response("report previously resolved")


# new: endpoints to reject previously approved reports to mark as appropriate
class ApproveToRejectReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.update_from_approve_to_reject()
            obj.save()
            return Response(self.get_serializer(obj).data)
        except Exception:
            return Response("report previously resolved")


# new: endpoints to approve previously rejected reports to mark as inappropriate
class RejectToApproveReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.update_from_reject_to_approve()
            obj.save()
            return Response(self.get_serializer(obj).data)
        except Exception:
            return Response("report previously resolved")
