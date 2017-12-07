from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

<<<<<<< HEAD
from danibraz.checkout.views import invoice_list, invoices_create, InvoiceUpdateView

urlpatterns = [
   # url(r'^pedido/novo/$', InvoiceFormView.as_view(), name='invoice_add'),
    url(r'^pedido/novo/$', invoices_create, name='invoice_add'),
=======
from danibraz.checkout.views import InvoiceFormView, InvoiceUpdateView, invoice_list, InvoiceCreateView
from danibraz.persons.views import clients_edit

urlpatterns = [
    #url(r'pedido/novo/$', lancamentos_create, name='lancamentos_create'),

    # url(r'pedidos/listar/$', lancamentos, name='lancamento_list'),
    # url(r'pedido/novo/$', lancamentos, name='lancamento'),
    url(r'^pedido/novo/$', InvoiceFormView.as_view(), name='invoice_add'),
    url(r'^pedido/novo2/$', InvoiceCreateView.as_view(), name='invoice_add2'),
    # url(r'pedido/editar/(?P<invoice_id>\d+)/$', InvoiceUpdateView, name='invoice_edit'),
>>>>>>> 4602188e886e7338a701ed8cec6e40a7379d83c1
    url(r'^pedido/editar/(?P<pk>\d+)/$$', InvoiceUpdateView.as_view(), name='invoice_edit'),
    url(r'pedido/listar/$', invoice_list, name='invoice_list'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
