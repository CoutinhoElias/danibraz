from django import forms
from django.core.exceptions import ValidationError
from material import *
from django.forms import inlineformset_factory, formset_factory, modelformset_factory

from danibraz.checkout.models import Invoice, Item, Papel
from danibraz.persons.models import Client


def validate_negative(value):
    if value == 3:
        raise ValidationError('Quantidade não pode ser maior que o estoque')


class ItemForm(forms.ModelForm):
    title = forms.ModelChoiceField(label='Titulo', required=True, queryset=Papel.objects.all())
    quantity = forms.IntegerField(label='Quantidade', validators=[validate_negative])


    class Meta:
        model = Item
        exclude = ['invoice', 'created', 'modified']
#///////////////////////////////////////////////////////////////////////////////////////////////////


class InvoiceForm(forms.models.ModelForm):

    class Meta:
        model = Invoice
        fields = '__all__'

ItemFormSet = inlineformset_factory(Invoice, Item, can_delete=True,
        fields=('title', 'quantity', 'unit_price'), extra=1)