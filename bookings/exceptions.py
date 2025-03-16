from shared.exceptions import DjBookingAPIError


class EndDateBeforeStartDateError(DjBookingAPIError):
    default_detail = "The end date must be after the start date."


class PastDateError(DjBookingAPIError):
    default_detail = "Booking dates must be in the future."


class PropertyAlreadyBookedError(DjBookingAPIError):
    default_detail = "This property is already booked for these dates"


class PaymentExpirationTimePassed(DjBookingAPIError):
    default_detail = "The time for payment has already passed. Please start the booking again."


class PaymentsUserMissingError(DjBookingAPIError):
    default_detail = (
        "Payments were not properly assigned to this user."
        + "Please make sure to go through all steps during registration."
    )


class BookingCannotBeCanceledError(DjBookingAPIError):
    default_detail = "This booking is not completed and it cannot be canceled at this time. Please try again later."


class PaymentProviderException(DjBookingAPIError):
    def __init__(self, message):
        super().__init__(detail=message)
