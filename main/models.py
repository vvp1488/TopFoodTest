from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_api_key.models import APIKey

CHECK_TYPE_CHOICES = (
        ('kitchen', 'чек для кухні'),
        ('client', 'чек для клієнта'),
    )


class Printer(models.Model):

    name = models.CharField('назва принтеру', max_length=50, unique=True)
    api_key = models.CharField('ключ доступу до API', max_length=255, unique=True, blank=True)
    check_type = models.CharField('тип чеку який друкує принтер', max_length=50, choices=CHECK_TYPE_CHOICES)
    point_id = models.IntegerField('точка до якої привязаний принтер', default=0)

    def __str__(self):
        return f'{self.name} - {self.check_type}'


class Check(models.Model):

    STATUS_CHOICES = (
        ('new', 'новий чек'),
        ('rendered', 'чек опрацьований'),
        ('printed', 'чек надрукований')
    )

    printer_id = models.ForeignKey(Printer, verbose_name='принтер', on_delete=models.PROTECT, related_name='checks', blank=True, null=True)
    type = models.CharField('тип чеку', choices=CHECK_TYPE_CHOICES, max_length=50, blank=True)
    order = models.JSONField('інформація про замовлення')
    order_number = models.CharField('номер замовлення', max_length=25)
    status = models.CharField('статус чеку', choices=STATUS_CHOICES, max_length=50, blank=True)
    pdf_file = models.FileField('посилання на створений PDF файл', upload_to='media/pdf/', blank=True)

    def __str__(self):
        return f'{self.id}'


@receiver(post_save, sender=Printer)
def generateApiKey(sender,instance, created, **kwargs):
    if created:
        new_api_key, key = APIKey.objects.create_key(name=f"{instance.name}")
        instance.api_key = key
        instance.save()















