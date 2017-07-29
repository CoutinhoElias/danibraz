import extra_views
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from material.admin.base import Inline
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from danibraz.persons.forms import ClientsForm, EmployeeForm
from danibraz.persons.models import Address, Client, Person
from material import *

class ItemInline(extra_views.InlineFormSet):
    model = Address #Model Address
    fields = '__all__'
    # Desnecessário
    #fields = ['id', 'qualificacao', 'campo_novo_um', 'campo_novo_dois', 'campo_novo_tres'] #Campos do endereço

    #Desnecessário
    # layout = Layout(
    #     # Campos do Persons
    #     Row('qualificacao', 'campo_novo_um'),
    #     Row('campo_novo_dois', 'campo_novo_tres'),
    #
    # )
    extra = 3# Define aquantidade de linhas a apresentar.

##
from django import forms
class PersonModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class AddressInline(extra_views.InlineFormSet):
    # form_class = AddressForm
    model = Address  # Model Address
    fields = '__all__'
    extra = 1
    can_delete = False
#

class NewProfissoesPessoaView(
                       extra_views.NamedFormsetsMixin,
                       extra_views.CreateWithInlinesView):
    model = Person
    form_class = PersonModelForm
    inlines = [AddressInline]
    inlines_names = ['endereco_inline']
    template_name = "persons/form_create_person_address.html"
    success_url = reverse_lazy("home")
    def get_success_url(self):
        sucess_url = super().get_success_url()
        print("Objeto salvo:")
        print(self.object)
        return sucess_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# class NewProfissoesPessoaView(LoginRequiredMixin,
#                               LayoutMixin,
#                       extra_views.NamedFormsetsMixin,
#                       extra_views.CreateWithInlinesView):
#
#     title = "Novo Cliente"
#     model = Person # model Person
#
#     #print('Chegou na linha 334')
#
#     layout = Layout(
#         # Campos do Persons
#         Fieldset("Inclua um cliente",
#                  Row('name', ),
#                  Row('birthday','purchase_limit'),
#                  Row('address1', ),
#                  ),
#         #Inline dos endereços
#         Inline('Endereços', ItemInline),
#     )
#     #print('Chegou na linha 340')
#
#     def forms_valid(self, form, inlines):
#         self.object = form.save(commit=False)
#         #self.object.pessoa_id = self.request.user.id
#         self.object.save()
#         return super(NewProfissoesPessoaView, self).forms_valid(form, inlines)
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()


def clients(request):
    if request.method == 'POST':
        form = ClientsForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/reserva/listagem/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'persons/person.html', {'form':form})
    else:
        context = {'form': ClientsForm()}
        return render(request, 'persons/person.html', context)

# def scheduling_edit(request, id_booking):
#     booking = Booking.objects.get(id=id_booking)
#     if request.method == 'GET':
#         form = BookingsForm(instance=booking)
#     else:
#         form = BookingsForm(request.POST, instance=booking)
#         if form.is_valid():
#             new = form.save(commit=False)
#             new.save()
#             form.save_m2m()
#         return HttpResponseRedirect('/reserva/listagem/')
#     return render(request, 'bookings/scheduling_form.html', {'form': form})


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