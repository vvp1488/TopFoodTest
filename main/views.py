from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import views, generics
from .serializers import PrinterListSerializer, CheckSerializer, OrderSerializer, PrinterDetailSerializer
from .models import Printer, Check
from .services import generateChecks
from .pagination import SmallPagesPaginator
from .tasks import generatePdfAsync
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_api_key.permissions import HasAPIKey


class PrinterListApiView(generics.ListAPIView):
    """GET запрос для відображення всіх принтерів"""
    queryset = Printer.objects.all().order_by('-id')
    serializer_class = PrinterListSerializer
    pagination_class = SmallPagesPaginator


class DetailPrinterCheckApiView(views.APIView):
    """GET запрос для відображення всих згенерованих чеків для конкретного принтера
    в headers в поле X-Api-Key потрібно передавати api-key принтеру
    """
    permission_classes = (HasAPIKey, )

    def get(self, request, pk):
        try:
            printer = Printer.objects.get(pk=pk)
        except Check.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PrinterDetailSerializer(printer)

        return Response(serializer.data)


class GeneratePdf(views.APIView):
    '''GET запрос міняє статус чека на "переглянутий"
    POST запрос друкує чек та міняє статус на "надрукований"
    permission with headers X-Api-Key: <your_printer_api_key>'''
    permission_classes = (HasAPIKey,)

    def get(self, request, pk, pk2):
        check = Check.objects.get(pk=pk2)
        if check.status == 'new':
            check.status = 'rendered'
            check.save()
        serializer = CheckSerializer(check)
        return Response(serializer.data)

    def post(self, request, pk, pk2):
        check = Check.objects.get(pk=pk2)
        if check.status == 'rendered' or 'new':
            check.status = 'printed'
            check.save()
        file_path = f'media/pdf/{check.order_number}_{check.type}.pdf'
        check.status = 'printed'
        check.save()
        file = open(file_path, 'rb')
        response = HttpResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=new.pdf'
        return response


@api_view(['POST'])
def generateOrder(request):
    '''POST запрос для генерації замовення, створення чеків для принтерів
    та запуску асинхронного воркера для генерації pdf
    Приклад запросу:
    {
    "point_id" : "1",
    "ingredients" : ["Cheese", "Салат", "Перець"],
    "order_number" : "672335189"

}
    '''
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            generateChecks(point_id=request.data['point_id'], ingredients=request.data['ingredients'], order_number=request.data['order_number'])
            check = Check.objects.filter(order=request.data['ingredients'], order_number=request.data['order_number']).values_list('pk')
            generatePdfAsync.delay(pk2=check[0][0])
            generatePdfAsync.delay(pk2=check[1][0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def htmltemplate(request, pk):
    check = Check.objects.get(pk=pk)
    context = {
        'check': check,
    }
    return render(request, 'base.html', context)
