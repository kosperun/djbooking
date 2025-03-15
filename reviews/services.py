from uuid import UUID

from bookings.models import Booking
from properties.selectors import property_retrieve
from reviews.exceptions import WrongBookingReferenceCode, WrongPropertyError
from reviews.models import Review
from users.models import User


def review_create(user: User, property_id: UUID, reference_code: str, text: str, score: int) -> Review:
    property = property_retrieve(property_id)
    booking = Booking.objects.filter(reference_code=reference_code).first()

    if booking is None or booking.user != user:
        raise WrongBookingReferenceCode()
    if booking.property != property:
        raise WrongPropertyError()

    review = Review(property=property, user=user, text=text, score=score)
    review.save()
    return review


def review_update(review: Review, **kwargs) -> Review:
    for field, value in kwargs.items():
        setattr(review, field, value)
    review.save()
    return review


def review_delete(review: Review) -> tuple:
    return review.delete()
