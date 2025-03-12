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
