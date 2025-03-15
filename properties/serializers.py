from decimal import Decimal

from rest_framework import serializers


class CountryCreateInputSerializer(serializers.Serializer):
    """Serializer to add a new country."""

    name = serializers.CharField()


class CountryOutputSerializer(serializers.Serializer):
    """Serializer to display a country's details."""

    id = serializers.UUIDField()
    name = serializers.CharField()


class CountryPaginatedOutputSerializer(serializers.Serializer):
    """Serializer to display a paginated list of countries."""

    count = serializers.IntegerField()
    results = CountryOutputSerializer(many=True)


class CountryUpdateInputSerializer(serializers.Serializer):
    """Serializer to accept input to update a country's details."""

    name = serializers.CharField()


class CityCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    region = serializers.CharField(required=False)


class CityUpdateInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    region = serializers.CharField(required=False)


class CityOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    country = CountryOutputSerializer()
    name = serializers.CharField()
    region = serializers.CharField(required=False)


class CityListPaginatedOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = CityOutputSerializer(many=True)


class PropertyCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    city_id = serializers.UUIDField()
    street = serializers.CharField()
    house_number = serializers.CharField()
    zip_code = serializers.CharField()
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=Decimal("0"))


class PropertyUpdateInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
    house_number = serializers.CharField(required=False)
    zip_code = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=Decimal("0"), required=False)


class PropertyCountryOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()


class PropertyCityOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    country = PropertyCountryOutputSerializer()
    region = serializers.CharField()


class PropertyOwnerOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()


class PropertyUserOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()


class PropertyCreateOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    type = serializers.CharField()
    owner = PropertyUserOutputSerializer()
    city = CityOutputSerializer()
    district = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.CharField()
    zip_code = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    capacity = serializers.IntegerField()
    number_of_rooms = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    created = serializers.DateTimeField()


class PropertyOutputSerializer(PropertyCreateOutputSerializer):
    average_rating = serializers.FloatField(required=False)


class PropertyShortOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    type = serializers.CharField()
    city = CityOutputSerializer()
    district = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.CharField()
    zip_code = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    capacity = serializers.IntegerField()
    number_of_rooms = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)


class PropertyListOutputSerializer(PropertyOutputSerializer):
    available = serializers.BooleanField(required=False)


class PropertyListPaginatedOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = PropertyListOutputSerializer(many=True)
