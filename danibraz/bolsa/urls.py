from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from danibraz.bolsa.views import importaPlanilha, planodecontas_list, upload_xls2, simple_upload

urlpatterns = [
    #url(r'^importar/$', importaPlanilha, name='importaPlanilha'),
    url(r'planodecontas/listar/$', planodecontas_list, name='planodecontas_list'),

    url(r'planodecontas/importar/$', simple_upload, name='simple_upload'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]



#AÇÃO DE IMPORTAR ==== /bolsa/importar/
#FORMULÁRIO DEIMPORTAR 1==== /bolsa/planodecontas/importar1/
#FORMULÁRIO DEIMPORTAR 2==== /bolsa/planodecontas/importar2/