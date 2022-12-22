from rest_framework import serializers
from .models import Printer, Check
from .validators import point_id_validator, order_number_validator


class PrinterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ('pk', 'name', 'api_key', 'check_type', 'point_id', 'checks')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('pk', 'type', 'order_number', 'status')


class PrinterDetailSerializer(serializers.ModelSerializer):
    checks = TestSerializer(many=True, read_only=True)

    class Meta:
        model = Printer
        fields = ('name', 'api_key', 'check_type', 'point_id', 'checks')


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('pk', 'printer_id', 'type', 'order', 'order_number', 'status')


class OrderSerializer(serializers.Serializer):
    point_id = serializers.IntegerField(validators=[point_id_validator])
    ingredients = serializers.JSONField()
    order_number = serializers.CharField(validators=[order_number_validator], min_length=9, max_length=9)




