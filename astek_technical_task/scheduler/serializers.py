from rest_framework import serializers

from astek_technical_task.scheduler.models import PredefinedTask
from astek_technical_task.api.serializers import ListSerializerSchema


class PredefinedTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedTask
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ListSerializerPredefinedTask(ListSerializerSchema):
    results = PredefinedTaskSerializer(many=True)