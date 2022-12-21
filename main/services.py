import os
from .models import Check, Printer
import requests
import datetime


def generateChecks(point_id, ingredients, order_number):
    kitchen_printer = Printer.objects.get(check_type='kitchen', point_id=point_id)
    client_printer = Printer.objects.get(check_type='client', point_id=point_id)
    client_check = Check.objects.create(printer_id=client_printer, type='client', order=ingredients, order_number=order_number, status='new')
    generateHtmlTemplateForPdf(client_check.pk)
    kitchen_check = Check.objects.create(printer_id=kitchen_printer, type='kitchen', order=ingredients, order_number=order_number, status='new')
    generateHtmlTemplateForPdf(kitchen_check.pk)


def generateHtmlTemplateForPdf(pk):
    req = requests.get(f'http://127.0.0.1:8000/check/{pk}/')
    check = Check.objects.get(pk=pk)
    file_path = f'templates/{datetime.date.today()}/{check.order_number}_{check.type}.html'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(req.content)


def generatePdfFromHtml(pk2):
    check = Check.objects.get(pk=pk2)
    file_path_html = f'templates/{datetime.date.today()}/{check.order_number}_{check.type}.html'
    files = {
        'content': open(file_path_html, 'rb'),
    }
    response = requests.post('http://0.0.0.0:5555/pdf', files=files)
    file_path_pdf = f'media/pdf/{datetime.date.today()}/{check.order_number}_{check.type}.pdf'
    os.makedirs(os.path.dirname(file_path_pdf), exist_ok=True)

    with open(file_path_pdf, 'wb') as f:
        f.write(response.content)

    check.status = 'printed'
    check.pdf_file = file_path_pdf
    check.save()


