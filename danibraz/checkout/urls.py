from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from danibraz.checkout.views import lancamentos_create

urlpatterns = [
    url(r'pedido/novo/$', lancamentos_create, name='lancamentos_create'),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
