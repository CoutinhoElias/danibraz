from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from danibraz.checkout.forms import ItemFormSet
from danibraz.checkout.forms import InvoiceForm
from danibraz.checkout.models import Invoice, Item


#///////////////////////////////////////////////////////////////////////////////////
#AJUSTAR DELETE E EDIT
def invoices_create(request):
    success_message = 'The invoice was edited correctly.'
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = ItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                invoice = form.save()
                formset.instance = invoice
                formset.save()

            return redirect('/lancamento/pedido/listar/')
    else:
        form = InvoiceForm()
        formset = ItemFormSet()

    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'checkout/invoice_form.html', context)


def invoices_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    print(request.method)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = ItemFormSet(request.POST, instance=invoice)

        #codigo_produto = int(request.POST['Invoice'])

        if form.is_valid() and formset.is_valid():

            #itemNota = Item.objects.filter(invoice_id=pk)
            #print("quantidade form:",formset.quantity)

            with transaction.atomic():
                #for item in itemNota:
                    #print("Nr:", item.invoice.pk, "Titulo:", item.title, "Qtd:", item.quantity, "Preço:",
                    #      item.unit_price)
                form.save()
                formset.save()

            return redirect('/lancamento/pedido/listar/')
    else:
        form = InvoiceForm(instance=invoice)
        formset = ItemFormSet(instance=invoice)

    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'checkout/invoice_form.html', context)

def invoices_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice.delete()
        return redirect('/lancamento/pedido/listar/')

    return render(request, 'invoices_delete.html', {'invoice': invoice})

#///////////////////////////////////////////////////////////////////////////////////
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'checkout/invoice_list.html', {'invoices': invoices})

