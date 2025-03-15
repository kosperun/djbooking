# from typing import Optional
#
# from bookings.models import Booking
# from properties.models import Property
# from properties.selectors import property_retrieve
# from reviews.models import Review
# from users.models import User

# def review_create(property_id: UUID, user: User, reference_code: str, text: str, score: int) -> Review:
#     property = property_retrieve(property_id)
#     booking = BookingRepository.get_by_reference_code(reference_code)
#
#     _validate_booking(user, property, booking)
#
#     review = Review(property=property, user=user, text=text, score=score)
#     review.save()
#     return review
#
#
# def _validate_booking(user: User, property: Property, booking: Optional[Booking]) -> None:
#     if booking is None or booking.user != user:
#         raise WrongBookingReferenceCode
#     if booking.property != property:
#         raise WrongPropertyError
#
#
# def review_update(review: Review, **kwargs) -> Review:
#     for field, value in kwargs.items():
#         setattr(review, field, value)
#     review.save()
#     return review
#
#
# def review_delete(review: Review) -> tuple:
#     return review.delete()
