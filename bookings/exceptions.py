from shared.exceptions import DjBookingAPIError


class EndDateBeforeStartDateError(DjBookingAPIError):
    default_detail = "The end date must be after the start date."


class PastDateError(DjBookingAPIError):
    default_detail = "Booking dates must be in the future."


class PropertyAlreadyBookedError(DjBookingAPIError):
    default_detail = "This property is already booked for these dates"


class BookingCannotBeCanceledError(DjBookingAPIError):
    default_detail = "This booking is not completed and it cannot be canceled at this time. Please try again later."
