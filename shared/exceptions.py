from rest_framework.exceptions import APIException


class DjBookingAPIError(APIException):
    """Base class for all API-related exceptions in djbooking."""

    status_code = 400
    default_detail = "An error occurred."
    default_code = "error"
