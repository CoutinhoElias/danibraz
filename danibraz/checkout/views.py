from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.models import Sum
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
    #invoice = get_object_or_404(Invoice, pk=pk)
    invoice = get_object_or_404(Invoice, pk=pk)
    print(request.method)
    if request.method == 'POST':
        #sub_brand = Item.objects.select_related('title').get(invoice_id=pk)
        #sub_brand = Item.objects.select_related('title').get(invoice_id=pk)

        form = InvoiceForm(request.POST, instance=invoice)
        formset = ItemFormSet(request.POST, instance=invoice)
        #formset = ItemFormSet(request.POST, sub_brand)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
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


def invoice_list(request):
    invoices = Invoice.objects.select_related('customer').all().order_by("emissao")
    return render(request, 'checkout/invoice_list.html', {'invoices': invoices})


def invoice_list_item(request):
    q = request.GET.get('search_box')
    print(request.GET)
    if q:
        print(q)
        items = Item.objects.select_related('title','invoice').all().filter(name__icontains=q)
    else:
        items = Item.objects.select_related('title', 'invoice').all().order_by('invoice__emissao')
        somatorios = {}

        for item in items:
            somatorio = somatorios.get(item.title, 0)

            if item.invoice.transaction_kind == 'in' or item.invoice.transaction_kind == 'eaj':
                somatorio += item.quantity
            else:
                somatorio -= item.quantity

            item.saldo = somatorio
            somatorios[item.title] = somatorio

    context = {'items': items}
    print(context)
    return render(request, 'checkout/item_list.html', context)

