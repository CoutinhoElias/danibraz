from django import forms
from django.core.exceptions import ValidationError
from material import *
from django.forms import inlineformset_factory


from danibraz.checkout.models import Lancamento, LancamentoItem, Invoice, Item, Papel
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
    #Campocalculado
    # total_prop = forms.DecimalField(widget=forms.TextInput(
    #     attrs={'class': 'form-control decimal-mask', 'readonly': True}), label='Total s/ imposto (R$)', required=False)
    total_prop = forms.DecimalField(label='Total s/ imposto (R$)', widget = forms.TextInput(attrs={'readonly':'readonly'}))

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        self.fields['total_prop'].localize = True
        self.fields['total_prop'].initial = '0.00' #Inicializa o campo com valor 0,00

    class Meta:
        model = Invoice
        exclude = ['total', 'created', 'modified']

    layout = Layout(
        # Campos do Persons
        Row(Span3('emissao'), Span9('customer'), ),
        Row('total_prop'),
    )


def validate_negative(value):
    if value == 3:
        raise ValidationError('Quantidade não pode ser maior que o estoque')


class ItemForm(forms.ModelForm):
    title = forms.ModelChoiceField(label='Titulo', required=True, queryset=Papel.objects.all())
    quantity = forms.IntegerField(label='Quantidade', validators=[validate_negative])

    # def clean_quantity(self):
    #     quantity = self.cleaned_data['quantity']
    #
    #     if quantity < 3:
    #         raise ValidationError('Quantidade não pode ser menor que 3')
    #     return quantity

    class Meta:
        model = Item
        exclude = ['invoice', 'created', 'modified']


ItemInvoiceFormSet = formset_factory(ItemForm, min_num=1, validate_min=True, extra=0, max_num=16, validate_max=True)

ItemInvoiceUpdateFormSet = modelformset_factory(Item, form=ItemForm, min_num=1, validate_min=True, extra=0,
                                                can_delete=True, max_num=16, validate_max=True)
