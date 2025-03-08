from rest_framework.exceptions import APIException


class DjBookingAPIError(APIException):
    """Base class for all API-related exceptions in djbooking."""

    status_code = 400
    default_detail = "An error occurred."
    default_code = "error"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        super().__init__(detail, code)
