from django.contrib import admin

from payments.models import PaymentUser


class PaymentUserAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "customer_id"]


admin.site.register(PaymentUser, PaymentUserAdmin)
