from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from .models import Movie, Rating, Report
from .serializers import MovieSerializer, ReviewSerializer, ReportSerializer, ReportUpdateSerializer
from .pagination import CustomPagination
from .filters import MovieFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

# Removes permissions from views


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

    def list(self, serializer):
        if not self.request.user.is_superuser:
            qs = Movie.objects.exclude(reports__status = 'INAPPROPRIATE')

        else:
            qs = Movie.objects.all()

        serializer = self.serializer_class(instance=qs, many=True)
        return Response({
            "data":serializer.data,
            "Message": "Success"
        },
        status=200)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = (IsAuthenticated,)

    # Movie can only be updated by its creator. And Also Check Other Authentication

    def update(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)

        user_info = self.request.user
        qs = self.queryset.filter(pk=int(self.kwargs.get('pk'))).last()

        new_title = request.data.get('title')

        if not qs:
            context = {
                'data': None,
                'message': 'Movie Not Found',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        if self.get_queryset().filter(title__iexact=request.data.get('title')).exclude(
                id=int(self.kwargs.get('pk'))).exists():

            context = {
                'data': None,
                'message': 'Movie Title is Already Found',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        title = request.data.pop("title")

        if serializer.is_valid():
            if not qs:
                context = {
                    'data': None,
                    'message': 'Movie Not Found',
                    'error': True, 'code': 400,
                }
                return Response(context, status=400)

            if qs.creator.username == user_info.username:
                qs = serializer.update(instance=self.get_object(
                ), validated_data=serializer.validated_data)
                if new_title:
                    qs.title = new_title
                    qs.save()

                serializer = self.serializer_class(instance=qs)

                context = {
                    'data': serializer.data,
                    'message': 'This is Not Your Movie',
                    'error': False, 'code': 200,
                }
                return Response(context, status=200)

            context = {
                'message': 'This is Not Your Movie',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        context = {
            'data': None,
            'message': 'Movie Can Not Update',
            'error': True, 'code': 400,
        }
        return Response(context, status=400)

    def delete(self, request, *args, **kwargs):
        qs = self.queryset.filter(pk=int(self.kwargs.get('pk')))
        if qs:
            qs.delete()
            context = {
                'message': 'Movie Delete Successfully',
                'error': False, 'code': 200,
            }
            return Response(context, status=200)

        return Response({'message': 'Movie is Not Found','error':True},
                        status=400)


class ListCreateReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        score = request.data.get('score')
        movie = request.data.get('movie')

        if not movie:
            return Response({'message': 'Movie ID is Required', 'error': True,
                             'code': 400},
                            status=400)
        if score < 1:
            return Response({'message': 'Score is Must Greater Than Or Equal 1', 'error': True,
                             'code': 400},
                            status=400)
        if score > 5:
            return Response({'message': 'Score is Must Less Than Or Equal 5', 'error': True},
                            status=400)

        review_qs = Rating.objects.filter(reviewer = self.request.user, movie= movie).last()
        if review_qs:
            return Response({'message': 'You Already Given Your Review','code':400, 'error': True},
                            status=400)
        movie_qs = Movie.objects.filter(pk = movie).last()

        if not movie_qs:
            return Response({'message': 'Movie is Not Found','code':400, 'error': True},
                            status=400)

        if serializer.is_valid():
            qs = serializer.save(reviewer=self.request.user)

            review_qs = self.queryset.filter(movie = movie)
            total_score = sum(review_qs.values_list('score', flat = True))
            avg_rating = float(total_score)/float(review_qs.count())

            movie_qs.avg_rating = round(avg_rating,2)
            movie_qs.save()

            serializer = ReviewSerializer(instance=movie_qs.movie.first())

        return Response({"data":serializer.data,
                         'message': 'Rating Add Successfully', 'error': False,
                         'code': 200},
                        status=200)


class RetrieveUpdateDestroyRatingAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        movie = request.data.get('movie')
        if movie:
            qs = Movie.objects.filter(pk = movie).last()
            if not qs:
                return Response({'message': 'Movie is Not Found', 'error': True},
                                status=400)

        user_info = self.request.user
        qs = self.queryset.filter(pk=int(self.kwargs.get('pk'))).last()

        if not qs:
            context = {
                'data': None,
                'message': 'Review is  Not Found',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        if serializer.is_valid():
            movie_qs = qs.movie

            if qs.reviewer.username == user_info.username:
                qs = serializer.update(instance=self.get_object(
                ), validated_data=serializer.validated_data)

                review_qs = self.queryset.filter(movie=qs.movie)
                total_score = sum(review_qs.values_list('score', flat=True))
                avg_rating = float(total_score) / float(review_qs.count())

                movie_qs.avg_rating = round(avg_rating, 2)
                movie_qs.save()

                serializer = ReviewSerializer(instance=movie_qs.movie.first())

                context = {
                    'data': serializer.data,
                    'message': 'Review Update Successfully',
                    'error': False, 'code': 200,
                }
                return Response(context, status=200)

            context = {
                'message': 'This is Not Your Review',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        context = {
            'data': None,
            'message': 'Review Can Not Update',
            'error': True, 'code': 400,
        }
        return Response(context, status=400)

    def delete(self, request, *args, **kwargs):
        qs = self.queryset.filter(pk=int(self.kwargs.get('pk')))
        if qs:
            qs.delete()
            context = {
                'message': 'Review Delete Successfully',
                'error': False, 'code': 200,
            }
            return Response(context, status=200)

        return Response({'message': 'Review is Not Found','error':True},
                        status=400)


class ListCreateReportAPIView(ListCreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        movie = request.data.get('movie')

        if not movie:
            return Response({'message': 'Movie ID is Required', 'error': True,
                             'code': 400},
                            status=400)

        report_qs = Report.objects.filter(reporter=self.request.user, movie=movie,
                                          ).exclude(status = 'REJECT').last()
        if report_qs:
            return Response({'message': 'You Already Given Your Report', 'code': 400, 'error': True},
                            status=400)
        movie_qs = Movie.objects.filter(pk=movie).last()

        if not movie_qs:
            return Response({'message': 'Movie is Not Found', 'code': 400, 'error': True},
                            status=400)

        if serializer.is_valid():
            qs = serializer.save(reporter=self.request.user)

            serializer = ReportSerializer(instance=qs)

        return Response({"data": serializer.data,
                         'message': 'Review Add Successfully', 'error': False,
                         'code': 200},
                        status=200)

    def list(self, serializer):
        if self.request.user.is_superuser:
            qs = Report.objects.all()
            serializer = ReportSerializer(instance=qs, many=True)
            return Response({
                "data": serializer.data,
                "Message": "Success"
            },
                status=200)

        else:
            return Response({
                "Message": "You Have Not Enough Permission",
                "code": 400,
            },
                status=400)



class RetrieveUpdateDestroyReportAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReportUpdateSerializer
    queryset = Report.objects.all()
    permission_classes = (IsAdminUser,)

    def update(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        movie = request.data.get('movie')
        status = request.data.get('status')
        if movie:
            qs = Movie.objects.filter(pk = movie).last()
            if not qs:
                return Response({'message': 'Movie is Not Found', 'error': True},
                                status=400)

        qs = self.queryset.filter(pk=int(self.kwargs.get('pk'))).last()

        if not qs:
            context = {
                'data': None,
                'message': 'Report is  Not Found',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        if not (status == 'INAPPROPRIATE' or status == 'REJECT' or status == 'UNRESOLVED'):
            context = {
                'message': 'Status Is Not Valid',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        if qs.status == status:
            return Response({
                'message': 'Status Is Already '+ str(status),
                'error': True, 'code': 400,
            }, status=400)

        if serializer.is_valid():

            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)

            serializer = ReportSerializer(instance=qs)

            context = {
                'data': serializer.data,
                'message': 'Review Update Successfully',
                'error': False, 'code': 200,
            }
            return Response(context, status=200)

            context = {
                'message': 'This is Not Your Review',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        context = {
            'data': None,
            'message': 'Review Can Not Update',
            'error': True, 'code': 400,
        }
        return Response(context, status=400)

    def delete(self, request, *args, **kwargs):
        qs = self.queryset.filter(pk=int(self.kwargs.get('pk')))
        if qs:
            qs.delete()
            context = {
                'message': 'Review Delete Successfully',
                'error': False, 'code': 200,
            }
            return Response(context, status=200)

        return Response({'message': 'Review is Not Found','error':True},
                        status=400)
