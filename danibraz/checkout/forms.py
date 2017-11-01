from django import forms
from django.forms import inlineformset_factory

from danibraz.checkout.models import Lancamento, LancamentoItem


class LancamentoForm(forms.models.ModelForm):

    class Meta:
        model = Lancamento
        fields = '__all__'

LancamentoItemFormSet = inlineformset_factory(Lancamento, LancamentoItem, can_delete=True,
        fields=('symbol', 'quantity','price'), extra=1)