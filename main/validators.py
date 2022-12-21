from .models import Printer, Check
from rest_framework import serializers


def point_id_validator(value):
    my_list = Printer.objects.filter().values_list('point_id').distinct()
    new_list = [x[0] for x in my_list]
    if value not in new_list:
        raise serializers.ValidationError('На даній точці не встановлено жодного принтера')


def order_number_validator(value):
    if Check.objects.filter(order_number=value).first():
        raise serializers.ValidationError(f'Чеки для замовлення {value} - вже були створені')