from shared.exceptions import DjBookingAPIError


class CountryMissingError(DjBookingAPIError):
    default_detail = "You must provide a country"


class WrongOwnerError(DjBookingAPIError):
    default_detail = "You cannot modify this property since you are not its owner."
