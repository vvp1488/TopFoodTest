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
    '''GET запрос міняє статус чека на переглянутий
    POST запрос запускає асинхронний вокер на завантаження(друк) чеку та зміна статусу чека'''
    permission_classes = (HasAPIKey,)

    def get(self, request, pk, pk2):
        check = Check.objects.get(pk=pk2)
        if check.status == 'new':
            check.status = 'rendered'
            check.save()
        serializer = CheckSerializer(check)
        return Response(serializer.data)

    def post(self, request, pk, pk2):
        generatePdfAsync.delay(pk2)
        return Response(data={"message": "all Done! Чек скачаний (надрукований)"})


@api_view(['POST'])
def generateOrder(request):
    '''POST запрос для генерації замовення, створення чеків для принтерів
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def htmltemplate(request, pk):
    check = Check.objects.get(pk=pk)
    context = {
        'check': check,
    }
    return render(request, 'base.html', context)