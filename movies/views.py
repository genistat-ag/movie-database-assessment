from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from .models import Movie,Rating,Report
from .serializers import MovieSerializer,ReviewSerializer,ReportSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
# Removes permissions from views


class ListOwnMovieView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get(self,request):
        try:
            queryset = Movie.objects.filter(creator=request.user)
            serializer_data = MovieSerializer(queryset,many=True)

            return Response(serializer_data.data,status=status.HTTP_200_OK)
        except Exception as e:
            response = {"message":str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



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


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        if Movie.objects.filter(id=serializer.data['id']).exists():
            get_data = Movie.objects.get(id=serializer.data['id'])
            if get_data.creator == self.request.user:
                 serializer_data = MovieSerializer(get_data,data=serializer.data)
                 if serializer_data.is_valid():
                    serializer_data.save()
                 else:
                    raise APIException(str(serializer_data.errors))
            else:
                raise APIException("user only can update own created movie")

class RetrieveUpdateDestroyRatingAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        if Rating.objects.filter(id=serializer.data['id']).exists():
            get_data = Rating.objects.get(id=serializer.data['id'])
            if get_data.reviewer == self.request.user:
                 serializer_data = ReviewSerializer(get_data,data=serializer.data)
                 if serializer_data.is_valid():
                    serializer_data.save()
                 else:
                    raise APIException(str(serializer_data.errors))
            else:
                raise APIException("user only can update own created movie")


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ListCreateReportAPIView(ListCreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryData = Report.objects.all()
        if self.request.user.is_superuser:
            return queryData

        else:
            raise APIException("only super user can generate all report list")


    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user,state="unresolved")

