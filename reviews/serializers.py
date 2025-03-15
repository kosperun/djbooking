from rest_framework import serializers

from properties.serializers import PropertyShortOutputSerializer


class UserReviewOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    nationality = serializers.CharField()


class ReviewOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = UserReviewOutputSerializer()
    text = serializers.CharField()
    score = serializers.IntegerField()
    created = serializers.DateTimeField()


class ReviewPaginatedListOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = ReviewOutputSerializer(many=True)


class MyReviewCreateInputSerializer(serializers.Serializer):
    property_id = serializers.UUIDField()
    reference_code = serializers.CharField()
    text = serializers.CharField()
    score = serializers.IntegerField()


class MyReviewUpdateInputSerializer(serializers.Serializer):
    text = serializers.CharField()
    score = serializers.IntegerField()


class MyReviewOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    property = PropertyShortOutputSerializer()
    text = serializers.CharField()
    score = serializers.IntegerField()
    created = serializers.DateTimeField()


class MyReviewsPaginatedListOutputSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    results = MyReviewOutputSerializer(many=True)
