from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from danibraz.checkout.views import InvoiceFormView, InvoiceUpdateView, invoice_list, InvoiceCreateView
from danibraz.persons.views import clients_edit

urlpatterns = [
    #url(r'pedido/novo/$', lancamentos_create, name='lancamentos_create'),

    # url(r'pedidos/listar/$', lancamentos, name='lancamento_list'),
    # url(r'pedido/novo/$', lancamentos, name='lancamento'),
    url(r'^pedido/novo/$', InvoiceFormView.as_view(), name='invoice_add'),
    url(r'^pedido/novo2/$', InvoiceCreateView.as_view(), name='invoice_add2'),
    # url(r'pedido/editar/(?P<invoice_id>\d+)/$', InvoiceUpdateView, name='invoice_edit'),
    url(r'^pedido/editar/(?P<pk>\d+)/$$', InvoiceUpdateView.as_view(), name='invoice_edit'),
    #url(r'^pedido/editar/(?P<invoice_id>\d+)/$', invoices_edit, name='invoice_edit'),
    #url(r'^pedido/listar/$', InvoiceSingleTableView.as_view(), name='invoice_list'),
    url(r'pedido/listar/$', invoice_list, name='invoice_list'),
    # url(r'pedido/editar/(?P<lancamento_id>\d+)/$', lancamentos_edit, name='lancamento_editar'),

    # url(r'^compras/$', ListadoCompras.as_view(), name="listado_compras"),
    # url(r'^crear_compra/$', CrearCompra.as_view(), name="crear_compra"),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
