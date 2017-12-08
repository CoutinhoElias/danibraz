from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from danibraz.checkout.views import invoice_list, invoices_create, invoices_update

urlpatterns = [
    #url(r'pedido/novo/$', lancamentos_create, name='lancamentos_create'),

    # url(r'pedidos/listar/$', lancamentos, name='lancamento_list'),
    # url(r'pedido/novo/$', lancamentos, name='lancamento'),

    # url(r'pedido/editar/(?P<invoice_id>\d+)/$', InvoiceUpdateView, name='invoice_edit'),
    url(r'^pedido/novo/$', invoices_create, name='invoice_add'),
    url(r'^pedido/editar/(?P<pk>\d+)$', invoices_update,name='invoice_edit'),
    url(r'pedido/listar/$', invoice_list, name='invoice_list'),


    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
