from django import forms
from material import *
from django.forms import inlineformset_factory


from danibraz.checkout.models import Lancamento, LancamentoItem, Invoice, Item
from danibraz.persons.models import Client

#sirleymacal@gmail.com
class LancamentoForm(forms.models.ModelForm):

    class Meta:
        model = Lancamento
        fields = '__all__'


LancamentoItemFormSet = inlineformset_factory(Lancamento, LancamentoItem, can_delete=True,
        fields=('symbol', 'quantity','price'), extra=1)

from django.forms import formset_factory, modelformset_factory

#-----------------------------------------------------------------------------------------------


class InvoiceForm(forms.ModelForm):
    customer = forms.ModelChoiceField(label='Pessoa', required=True, queryset=Client.objects.all())
    emissao = forms.DateField(label='Emissão', required=False,
                              widget=forms.TextInput(attrs={'class':'datepicker picker__input picker__input--active'}))
    class Meta:
        model = Invoice
        #fields = '__all__'
        exclude = ['total', 'created', 'modified']

    layout = Layout(
        # Campos do Persons
        Row(Span3('emissao'), Span9('customer'), ),
    )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['invoice', 'created', 'modified']


ItemInvoiceFormSet = formset_factory(ItemForm, min_num=1, validate_min=True, extra=0, max_num=16, validate_max=True)

ItemInvoiceUpdateFormSet = modelformset_factory(Item, form=ItemForm, min_num=1, validate_min=True, extra=0,
                                                can_delete=True, max_num=16, validate_max=True)
