from shared.exceptions import DjBookingAPIError


class UserDoesNotExist(DjBookingAPIError):
    default_detail = "Such user does not exist"


class MissingTokenOrEmail(DjBookingAPIError):
    default_detail = "Token and/or email is missing"


class RegistrationTimePassed(DjBookingAPIError):
    default_detail = "Your sign up time has already passed. Please start registration again."
