from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating, Report
from .serializers import MovieSerializer, ReviewSerializer, ReportSerializer, CreateReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


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
        # print('data = ', data)
        # Assign the movie in report
        # Report.objects.create(movie=data, reporter=self.request.user)

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


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        print("data = ", self.request.data)
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        query = super().get_queryset()
        return query


class RetrieveUpdateDestroyReviewAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


class ListCreateReportAPIView(ListCreateAPIView):
    serializer_class = CreateReportSerializer
    queryset = Report.objects.all()

    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class ReportReview(UpdateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAdminUser]


class ApproveReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.status = "inappropriate"
            obj.save()
            return Response(self.get_serializer(obj).data)
        except:
            return Response('already updated')


class RejectReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.status = "reject"
            obj.save()
            return Response(self.get_serializer(obj).data)
        except:
            return Response('already updated')


class ApproveToRejectReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.status = "reject"
            obj.save()
            return Response(self.get_serializer(obj).data)
        except:
            return Response('already updated')


class RejectToApproveReportAPIView(ReportReview):
    def update(self, request, *arg, **kwargs):
        obj = self.get_object()
        try:
            obj.status = "inappropriate"
            obj.save()
            return Response(self.get_serializer(obj).data)
        except:
            return Response('already updated')
