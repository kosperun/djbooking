from django.contrib import admin

from bookings.models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "property", "date_from", "date_to", "status"]


admin.site.register(Booking, BookingAdmin)
