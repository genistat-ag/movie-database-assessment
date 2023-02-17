from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    size = 10
    size_query_param = 'page_size'
