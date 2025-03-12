from django.contrib import admin

from properties.models import City, Country, Property, PropertyImage


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "region"]


class PropertyAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "city", "type", "capacity", "number_of_rooms", "price"]


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage)
