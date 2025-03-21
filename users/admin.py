from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "first_name"]


admin.site.register(User, UserAdmin)
