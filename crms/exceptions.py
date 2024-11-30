# exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add custom logic for specific exceptions
    if response is not None:
        # Example: Customize the response for authentication errors
        if response.status_code == 401:
            response.data = {
                'error': 'Authentication credentials were not provided or are invalid.'
            }
        elif response.status_code == 403:
            response.data = {
                'error': 'You do not have permission to perform this action.'
            }
        elif response.status_code == 400:
            response.data = {
                'error': 'Bad request: Please check your input.'
            }
        # You can add more customizations for other status codes here

    return response