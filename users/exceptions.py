from shared.exceptions import DjBookingAPIError


class UserDoesNotExist(DjBookingAPIError):
    detail = "Such user does not exist"
