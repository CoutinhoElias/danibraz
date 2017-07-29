from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog
from danibraz.persons.views import clients, employees, NewProfissoesPessoaView

urlpatterns = [
    url(r'clientes/$', clients, name='clients'),
    url(r'cliente/$', NewProfissoesPessoaView.as_view(), name='clients'),
    url(r'funcionarios/$', employees, name='employees'),
    #url(r'cliente$', NewProfissoesPessoaView.as_view(template_name="person_and_professions.html")),
    #url(r'qqcoisa/$', NewShipmentView, name='shipment_new'),

    #url(r'editar/(?P<id_booking>\d+)/$', scheduling_edit, name='scheduling_edit'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
