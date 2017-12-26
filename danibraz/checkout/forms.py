from django import forms
from django.forms import inlineformset_factory

from danibraz.checkout.models import Item, Invoice


class ItemForm(forms.ModelForm):
    title = forms.ChoiceField(label='Titulo', required=True)
    quantity = forms.IntegerField(label='Quantidade')

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].localize = True

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