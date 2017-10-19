import extra_views
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from material import *
# Create your views here.
from danibraz.persons.forms import ClientsForm, EmployeeForm, AddressForm
from danibraz.persons.models import Address, Person, Client


from django.db.models import Q

#from danibraz.persons.forms import ClientsForm, EmployeeForm



class AddressInline(extra_views.InlineFormSet):
    model = Address #Model Address
    fields = ['kynd', 'public_place', 'number', 'city', 'state', 'zipcode', 'country', 'phone', ]
    extra = 1
    can_delete = True


#LoginRequiredMixin faz a mesma função de @login_required(login_url=LOGIN_URL). a ndiferença que LoginRequiredMixin não precisa apontar na url
class NewCadastroPessoaView(LayoutMixin,
                      extra_views.NamedFormsetsMixin,
                      extra_views.CreateWithInlinesView):
    title = "Nova Pessoa 87"

    model = Person# model Person

    layout = Layout(
        # Campos do Persons
        Fieldset("Inclua uma pessoa",
                 Row('name', ),
                 Row('birthday','purchase_limit'),
                 Row('address1', ),
                 ),
        #Inline dos endereços
        Inline('Endereços 98', AddressInline,),

    )

    #print('Chegou na linha 340')

    def forms_valid(self, form, inlines):
        self.object = form.save(commit=False)
        #self.object.person_id = self.request.user.id
        self.object.save()
        return super(NewCadastroPessoaView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return self.object.get_absolute_url()
"""--------------------------------------------------------------------------------------------------"""

class AddressInline1(extra_views.InlineFormSet):
    model = Address #Model Address
    fields = ['kynd', 'public_place', 'number', 'city', 'state', 'zipcode', 'country', 'phone', ]
    extra = 1
    can_delete = True


#LoginRequiredMixin faz a mesma função de @login_required(login_url=LOGIN_URL). a ndiferença que LoginRequiredMixin não precisa apontar na url
class NewCadastroPessoaView1(LayoutMixin,
                      extra_views.NamedFormsetsMixin,
                      extra_views.CreateWithInlinesView):
    title = "Nova Pessoa 87"

    model = Person# model Person

    layout = Layout(
        # Campos do Persons
        Fieldset("Inclua uma pessoa",
                 Row('name', ),
                 Row('birthday','purchase_limit'),
                 Row('address1', ),
                 ),
        #Inline dos endereços
        Inline('Endereços SEMFORM', AddressInline,),

    )

    #print('Chegou na linha 340')

    def forms_valid(self, form, inlines):
        self.object = form.save(commit=False)
        #self.object.person_id = self.request.user.id
        self.object.save()
        return super(NewCadastroPessoaView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return self.object.get_absolute_url()

"""--------------------------------------------------------------------------------------------------"""


# def clients_list(request):
#     context = {
#         'clients_list': Client.objects.all()
#     }
#     return render(request, 'persons/person_list.html', context)

def clients_list(request):
    q = request.GET.get('search_box')
    if q:
        clients = Client.objects.filter(Q(name__icontains=q))
    else:
        clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'persons/person_list.html', context)



def clients(request):
    if request.method == 'POST':

        form = ClientsForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
            return redirect(new)
            #return HttpResponseRedirect('/reserva/listagem/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'persons/person.html', {'form':form})
    else:
        context = {'form': ClientsForm()}
        return render(request, 'persons/person.html', context)


def clients_edit(request, person_id):
    pessoa = get_object_or_404(Client, pk=person_id)
    if request.method == 'POST':
        form = ClientsForm(request.POST, instance=pessoa)
        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()
            return HttpResponseRedirect('/cadastro/clientes/editar/'+person_id, person_id)
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'persons/person.html', {'form':form})
    else:
        print('Entrou emm odo de edição do cliente '+person_id)

        request.session['person_id'] = person_id
        print('A variável person_id da session já possui o valor: '+request.session['person_id'])
        #return HttpResponseRedirect('/cadastro/clientes/listar/')
        context = {'form': ClientsForm(instance=pessoa)}
        return render(request, 'persons/person.html', context)


def employees(request):
    if request.method == 'POST':

        form = EmployeeForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/reserva/listagem/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'persons/person.html', {'form':form})
    else:
        context = {'form': EmployeeForm()}
        return render(request, 'persons/person.html', context)


def address(request):
    if 'person_id' in request.session:

        if request.method == 'POST':
            #request.session['elias'] = 'cabeção'
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'+ request.session['person_id'])

            form = AddressForm(request.POST)

            if form.is_valid():
                print('<<<<==== FORM VALIDO ====>>>>')
                new = form.save()

                return HttpResponseRedirect('/cadastro/clientes/editar/'+request.session["person_id"])
            else:
                print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
                print(form)
                return render(request, 'persons/person_address.html', {'form':form})
        else:
            person_instance = Person.objects.get(pk=request.session["person_id"])
            initial_data = {"person": person_instance}
            context = {'form': AddressForm(initial=initial_data)}

            return render(request, 'persons/person_address.html', context)
    else:
        return HttpResponseRedirect('/cadastro/clientes/listar/') #fuincionando mais ou menos, verificar o motivo de estar caindoaqui
