from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from danibraz.bolsa.views import importaPlanilha, planodecontas_list, simple_upload, planodecontas_export

urlpatterns = [
    #url(r'^importar/$', importaPlanilha, name='importaPlanilha'),
    url(r'planodecontas/listar/$', planodecontas_list, name='planodecontas_list'),

    url(r'planodecontas/importar/$', simple_upload, name='simple_upload'),
    url(r'planodecontas/exportar/$', planodecontas_export, name='planodecontas_export'),



    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]



#AÇÃO DE IMPORTAR ==== /bolsa/importar/
#FORMULÁRIO DEIMPORTAR 1==== /bolsa/planodecontas/importar1/
#FORMULÁRIO DEIMPORTAR 2==== /bolsa/planodecontas/importar2/