from django.utils import timezone
from rest_framework import serializers

from core.models import (Employee, Enterprise, Site, Tag, PatrolLog, Planning, Zone)


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ['id', 'designation', 'created', 'modified']


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'designation', 'enterprise', 'created', 'modified']


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'designation', 'site', 'created', 'modified']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'designation', 'code_pin', 'site', 'created', 'modified']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'zone', 'code_nfc', 'designation', 'order', 'observation', 'created', 'modified']


class PatrolLogSerializer(serializers.ModelSerializer):
    zone_id = serializers.CharField(
        source='tag.zone.id',
        read_only=True,
        label='Zone ID'
    )
    zone__designation = serializers.CharField(
        source='tag.zone.designation',
        read_only=True,
        label='Zone'
    )
    tag__designation = serializers.CharField(source='tag.designation', read_only=True)
    tag__order = serializers.CharField(source='tag.order', read_only=True)
    now = serializers.SerializerMethodField()

    @staticmethod
    def get_now(obj):
        return timezone.now()

    class Meta:
        model = PatrolLog
        fields = ['id', 'tag', 'audio_path', 'image_path', 'description_anomaly', 'zone_id', 'zone__designation',
                  'tag__designation', 'tag__order', 'is_checked', 'created', 'modified', 'now', 'check_datetime',
                  'check_tolerance', 'checked_datetime', 'checked_by'
                  ]


class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = '__all__'
