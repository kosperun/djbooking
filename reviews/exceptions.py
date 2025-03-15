from shared.exceptions import DjBookingAPIError


class WrongBookingReferenceCode(DjBookingAPIError):
    default_detail = (
        "We couldn't find a booking with this reference code among your bookings. "
        + "Make sure that you entered a correct reference code."
    )


class WrongPropertyError(DjBookingAPIError):
    default_detail = (
        "This code refers to another lodging that you stayed in. "
        + "Please enter the correct code or select another lodging for review."
    )
