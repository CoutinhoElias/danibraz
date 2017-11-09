from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from danibraz.checkout.views import InvoiceFormView
from danibraz.persons.views import clients_edit

urlpatterns = [
    #url(r'pedido/novo/$', lancamentos_create, name='lancamentos_create'),

    # url(r'pedidos/listar/$', lancamentos, name='lancamento_list'),
    # url(r'pedido/novo/$', lancamentos, name='lancamento'),
    url(r'^pedido/novo/$', InvoiceFormView.as_view(), name='invoice_add'),
    # url(r'pedido/editar/(?P<lancamento_id>\d+)/$', lancamentos_edit, name='lancamento_editar'),

    # url(r'^compras/$', ListadoCompras.as_view(), name="listado_compras"),
    # url(r'^crear_compra/$', CrearCompra.as_view(), name="crear_compra"),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
