from django import forms
from django.forms import Form
from material import Layout, Fieldset, Row, Span6

from danibraz.persons.models import Client


# class ClientsForm(forms.ModelForm):
#     name = forms.CharField(label='Nome', required=True)
#     birthday = forms.DateField(label='Nascimento', required=False)
#     address = forms.CharField(label='Endereço completo')
#     purchase_limit = forms.DecimalField(label='Limite de compra')
#     compra_sempre = forms.BooleanField(label='Compra sempre?', required=False)
#
#     class Meta:
#         model = Client
#         fields = '__all__'
#
#     layout = Layout(
#         Fieldset("Inclua um cliente",
#                  Row('name', ),
#                  Row('birthday','purchase_limit'),
#                  Row('address', ),
#                  Row('compra_sempre', ),
#                  )
#     )


class EmployeeForm(forms.ModelForm):
    name = forms.CharField(label='Nome', required=True)
    birthday = forms.DateField(label='Nascimento', required=False)
    address = forms.CharField(label='Endereço completo')
    purchase_limit = forms.DecimalField(label='Limite de compra')
    ctps = forms.CharField(label='Carteira de trabalho', required=False)
    salary = forms.DecimalField(label='Salário')

    class Meta:
        model = Client
        fields = '__all__'

    layout = Layout(
        Fieldset("Inclua um funcionário",
                 Row('name', ),
                 Row(Span6('birthday'), Span6('ctps'), ),
                 Row(Span6('purchase_limit'),Span6('salary'),),
                 Row('address', ),
                 )
    )


# class AddressForm(forms.Form):
#     person = forms.CharField(max_length=250)
#     public_place = forms.CharField(max_length=250)
#     number = forms.CharField(max_length=100)
#     city = forms.CharField(max_length=100)
#     state = forms.CharField(max_length=10)
#     zipcode = forms.CharField(max_length=10)
#     country = forms.CharField(max_length=10)
#     phone = forms.CharField(max_length=10)
#
#     class Meta:
#         model = Address
#         exclude = ['person']
#
#     layout = Layout(
#         'public_place',
#         'number',
#         'city',
#         Row('state', 'zipcode'),
#         Row('country', 'phone'),
#     )

# AddressFormSet = formset_factory(AddressForm, extra=3, can_delete=True)

