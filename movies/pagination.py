from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    # PageNumberPagination does not have built-in size attribute it has page_size for pagination
    page_size = 10  
    # PageNumberPagination does not have built-in size_query_param attribute it has page_size_query_param for pagination
    page_size_query_param = 'page_size' 
