from rest_framework import serializers
from logger.models import *
from django.contrib.auth.models import User
from agents.models import Profile, Room, Building
from django_celery_results.models import TaskResult

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'building', 'join_date', 'description',)

    def update(self, instance, validated_data):
        instance.push_notification_token = validated_data.get(
            'push_notification_token', instance.geofencing_active)
        instance.username = validated_data.get(
            'username', instance.username)
        geo_enablel = validated_data.get(
            'geofencing_active', instance.geofencing_active)
        if geo_enablel == "true":
            instance.geofencing_active = True
        elif geo_enablel == "false":
            instance.geofencing_active = False

        notification_enable = validated_data.get(
            'notification_active', instance.notification_active)
        if notification_enable == "true":
            instance.notification_active = True
        elif notification_enable == "false":
            instance.notification_active = False

        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('name', 'user_number',)

    def update(self, instance, validated_data, profile):
        if validated_data.get('control_mode', instance.control_mode) == "Manuel" or validated_data.get('control_mode', instance.control_mode) == "Manual":
            instance.control_mode = "Manual"
        else:
            instance.control_mode = validated_data.get('control_mode', instance.control_mode)
        instance.temperature_setpoint = validated_data.get(
            'temperature_setpoint', instance.temperature_setpoint)
        instance.last_change_by_user = profile

        instance.save()
        return instance


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = ['value', 'time']


class MetadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetaData
        fields = ["table_id", "topic", "data_point_name",
                  "data_point_type", "measurement_type", "description"]

class TaskResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskResult
        fields = '__all__'
