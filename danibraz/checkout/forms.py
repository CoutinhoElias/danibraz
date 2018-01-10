from django import forms
from django.forms import inlineformset_factory

from danibraz.checkout.models import Item, Invoice
from danibraz.static.material import Layout, Row


# class ItemForm(forms.models.ModelForm):
#     title = forms.ChoiceField(label='Titulo', required=True)
#     quantity = forms.IntegerField(label='Quantidade')
#     total = forms.DecimalField(label='Total', widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    # def __init__(self, *args, **kwargs):
    #     super(ItemForm, self).__init__(*args, **kwargs)
    #     self.fields['quantity'].localize = True

    # class Meta:
    #     model = Item
    #     exclude = ['invoice', 'created', 'modified']
#///////////////////////////////////////////////////////////////////////////////////////////////////


class InvoiceForm(forms.models.ModelForm):

    class Meta:
        model = Invoice
        fields = '__all__'

    layout = Layout(
                 Row('transaction_kind','emissao'),
                 Row('customer', 'total')
                 )

ItemFormSet = inlineformset_factory(Invoice, Item, can_delete=True,
        fields=('title', 'quantity', 'unit_price', 'other_costs'), extra=1)