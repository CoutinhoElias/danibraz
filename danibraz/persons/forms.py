from material import *

from danibraz.persons.models import Client, Employee, Person, Address

from django import forms

#from danibraz.persons.views import AddressInline


class ClientsForm(forms.ModelForm):
    name = forms.CharField(label='Nome', required=True)
    birthday = forms.DateField(label='Nascimento', required=False)
    address1 = forms.CharField(label='Endereço completo')
    purchase_limit = forms.DecimalField(label='Limite de compra')
    compra_sempre = forms.BooleanField(label='Compra sempre?', required=False)

    class Meta:
        model = Client
        fields = '__all__'

    layout = Layout(
        Fieldset("Inclua um cliente",
                 Row('name', ),
                 Row('birthday','purchase_limit'),
                 Row('address1', ),
                 Row('compra_sempre', ),
                 )
    )


class EmployeeForm(forms.ModelForm):
    name = forms.CharField(label='Nome', required=True)
    birthday = forms.DateField(label='Nascimento', required=False)
    address1 = forms.CharField(label='Endereço completo')
    purchase_limit = forms.DecimalField(label='Limite de compra')
    ctps = forms.CharField(label='Carteira de trabalho', required=False)
    salary = forms.DecimalField(label='Salário')

    class Meta:
        model = Employee
        fields = '__all__'

    layout = Layout(
        Fieldset("Inclua um funcionário",
                 Row('name', ),
                 Row(Span6('birthday'), Span6('ctps'), ),
                 Row(Span6('purchase_limit'),Span6('salary'),),
                 Row('address1', ),
                 )
    )


"""----------------------------------------------------------------------------------"""

class PersonForm(forms.ModelForm):
    name = forms.CharField(label='Nome', required=True)
    birthday = forms.DateField(label='Nascimento', required=False)
    address1 = forms.CharField(label='Endereço completo')
    purchase_limit = forms.DecimalField(label='Limite de compra')

    class Meta:
        model = Person
        fields = '__all__'

    layout = Layout(
        # Campos do Persons
        Fieldset("Inclua uma pessoa",
                 Row('name', ),
                 Row('birthday','purchase_limit'),
                 Row('address1', ),
                 ),
        #Inline dos endereços
        #Inline('Endereços Com form', AddressInline,),

    )

KIND = (
    (None, 'Selecione o Tipo'),
    ('P', 'PRINCIPAL'),
    ('C', 'COBRANÇA'),
    ('E', 'ENTREGA'))


class AddressForm(forms.ModelForm):
    person = forms.ModelChoiceField(label='Pessoa', required=True, queryset=Person.objects.all())
    kynd = forms.ChoiceField(label='Tipo de endereço',choices=KIND)
    public_place = forms.CharField(label='Endereço completo')
    number = forms.CharField(label='Número')
    city = forms.CharField(label='Cidade')
    state = forms.CharField(label='Estado')
    zipcode = forms.CharField(label='Cep')
    country = forms.CharField(label='País')
    neighborhood = forms.CharField(label='Bairro')

    class Meta:
        model = Address
        fields = '__all__'

    layout = Layout(
        # Campos do Persons
        Fieldset("Inclua um endereço",
                 Row('person'),
                 Row('zipcode', 'neighborhood', 'kynd'),
                 Row(Span8('public_place'),Span4('number')),
                 Row(Span7('city'),Span5('state'),),
                 Row('country', ),
                 ),
    )