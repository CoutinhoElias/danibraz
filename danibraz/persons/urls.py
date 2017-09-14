from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog

from danibraz.persons import views
#from danibraz.persons.views import #clients, employees#, NewProfissoesPessoaView
from danibraz.persons.views import employees, clients, clients_edit, address, clients_list

urlpatterns = [
    #url(r'cliente/$', NewProfissoesPessoaView.as_view(), name='clients'),
    url(r'^pessoa/', views.NewCadastroPessoaView1.as_view(template_name="persons/person_and_professions.html")),
    url(r'^pessoas/', views.NewCadastroPessoaView.as_view(template_name="persons/form.html")),

    url(r'funcionarios/$', employees, name='employees'),

    # url(r'clientes/editar/(?P<person_id>\d+)/endereco/$', address, name='address'),
    url(r'clientes/endereco/novo/$', address, name='address'),

    url(r'clientes/listar/$', clients_list, name='clients_list'),
    url(r'clientes/$', clients, name='clients'),
    url(r'clientes/editar/(?P<person_id>\d+)/$', clients_edit, name='clients_editar'),

    #url(r'cliente$', NewProfissoesPessoaView.as_view(template_name="person_and_professions.html")),
    #url(r'qqcoisa/$', NewShipmentView, name='shipment_new'),

    #url(r'editar/(?P<id_booking>\d+)/$', scheduling_edit, name='scheduling_edit'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
