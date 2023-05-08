from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView

from .filters import MovieFilter
from .pagination import CustomPagination
from .models import Movie, Rating, Report
from .permissions import IsOwnerOrReadOnly
from .serializers import MovieSerializer, ReviewSerializer, ReportSerializer, CreateReportSerializer

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
    
    def get_queryset(self):
        query = super().get_queryset()
        ids = []
        for i in query:
            if i.status == 'inappropriate':
                if i.creator == self.request.user:
                    ids.append(i.id)
            else:
                ids.append(i.id)
        return query.filter(id__in=ids)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ['get', 'put', 'delete']


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    http_method_names = ['get', 'put', 'delete']


class ListCreateReportAPIView(ListCreateAPIView):
    serializer_class = CreateReportSerializer
    queryset = Report.objects.all()

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.request.method == 'POST':
            self.permission_classes= [IsAuthenticated]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class ReportReview(UpdateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAdminUser]
    http_method_names = ['put']


class ApproveReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.approve()
            obj.save()
            return Response(self.get_serializer(obj).data)
        except:
            return Response('already updated')


class RejectReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.reject()
            obj.save()
            return Response(self.get_serializer(obj).data)
        except:
            return Response('already updated')


class ApproveToRejectReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.approveToReject()
            obj.save()
            return Response(self.get_serializer(obj).data)
        except:
            return Response('already updated')


class RejectToApproveReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.rejectToApprove()
            obj.save()
            return Response(self.get_serializer(obj).data)
        except:
            return Response('already updated')
