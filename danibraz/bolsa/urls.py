from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from danibraz.bolsa.views import importaPlanilha, planodecontas_list, upload_xls

urlpatterns = [
    url(r'^importar/$', importaPlanilha, name='importaPlanilha'),
    url(r'planodecontas/listar/$', planodecontas_list, name='planodecontas_list'),
    url(r'planodecontas/importar/$', upload_xls, name='upload_xls'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
