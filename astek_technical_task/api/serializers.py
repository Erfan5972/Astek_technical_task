from rest_framework import serializers


class PaginationParamsSerializer(serializers.Serializer):
    limit = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=100,
        help_text="Number of results to return per page. Default is 10. Max is 50."
    )
    offset = serializers.IntegerField(
        required=False,
        min_value=0,
        help_text="The initial index from which to return the results. Default is 0."
    )


class ListSerializerSchema(serializers.Serializer):
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    results = serializers.ListField(child=serializers.DictField())