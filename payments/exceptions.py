from shared.exceptions import DjBookingAPIError


class PaymentExpirationTimePassed(DjBookingAPIError):
    default_detail = "The time for payment has already passed. Please start the booking again."


class PaymentsUserMissingError(DjBookingAPIError):
    default_detail = (
        "Payments were not properly assigned to this user."
        + "Please make sure to go through all steps during registration."
    )


class PaymentProviderException(DjBookingAPIError):
    def __init__(self, message):
        super().__init__(detail=message)
