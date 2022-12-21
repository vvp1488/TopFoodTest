from django.contrib import admin
from .models import Check, Printer

admin.site.register(Printer)


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_filter = ("printer_id", "type", "status", )