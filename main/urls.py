from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    PrinterListApiView,
    generateOrder,
    htmltemplate,
    DetailPrinterCheckApiView,
    GeneratePdf
)

schema_view = get_schema_view(
   openapi.Info(
      title="Printers and Checks",
      default_version='v1',
      description="Api service for generate checks",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api-auth/', include('rest_framework.urls')),
    path('printer-list/', PrinterListApiView.as_view()),
    path('printer-list/<int:pk>/', DetailPrinterCheckApiView.as_view()),
    path('printer-list/<int:pk>/<int:pk2>/', GeneratePdf.as_view()),
    path('neworder/', generateOrder),
    path('check/<int:pk>/', htmltemplate),
    path('download/<int:pk/'),
]
