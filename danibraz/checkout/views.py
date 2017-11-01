from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from danibraz.checkout.forms import LancamentoForm, LancamentoItemFormSet


def lancamentos_create(request):
    if request.method == 'POST':
        form = LancamentoForm(request.POST)
        formset = LancamentoItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                lancamentoItem = form.save()
                formset.instance = lancamentoItem
                formset.save()

            return redirect('/teams/')
    else:
        form = LancamentoForm()
        formset = LancamentoItemFormSet()

    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'checkout/lancamentos_edit_material.html', context)