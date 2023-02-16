from rest_framework.exceptions import APIException
from rest_framework import status

class UserNotMatchedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'User not matched'
    default_code = 'user_not_matched'


class MyCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An error occurred while processing your request.'
    default_code = 'custom_error'