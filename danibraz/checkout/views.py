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
        items = Item.objects.select_related('title','invoice').all().order_by('invoice__emissao').filter(name__icontains=q)
    else:
        items = Item.objects.select_related('title', 'invoice').all().order_by('invoice__emissao')

        estoques = {}
        acumulados_estoques = {}

        tipo_anterior = 'in'

        for item in items:

            somatorio = estoques.get(item.title, 0)
            acumulado = acumulados_estoques.get(item.title, 0)


            if item.invoice.transaction_kind in('in','eaj'):
                somatorio += item.quantity #Calcula o estoque
                acumulado += (item.quantity * item.unit_price + item.other_costs)

                acumulado_anterior = somatorio - item.quantity  # Resolvido

                if tipo_anterior not in('in','eaj'):
                    preco_medio_anterior = preco_medio_anterior
                    #preco_medio_anterior = (acumulado - item.total) / ((somatorio - item.quantity) + quantidade_anterior)
                    print('Se tipo_anterior =', tipo_anterior, 'Preçomédioanterior <=> ', preco_medio_anterior,)

                    preco_medio_atual = (acumulado_anterior * preco_medio_anterior + item.total) / somatorio

                    item.pmedio = preco_medio_atual
                else:
                    preco_medio_anterior = acumulado / somatorio
                    print('Se tipo_anterior =', tipo_anterior, 'Preçomédioanterior = ', acumulado, '/', somatorio)

                    preco_medio_atual = (acumulado / somatorio)

                    item.pmedio = preco_medio_atual

                    print(item.pmedio, ' = ', acumulado, '/', somatorio)

                tipo_anterior = item.invoice.transaction_kind
            else:
                somatorio -= item.quantity
                acumulado_anterior = somatorio + item.quantity  # Resolvido

                if tipo_anterior not in('out','saj'):
                    preco_medio_anterior = preco_medio_atual
                    print('Se tipo_anterior =', tipo_anterior, 'Preçomédioanterior = preco_medio_atual', preco_medio_atual)

                    preco_medio_atual = preco_medio_atual

                    item.pmedio = preco_medio_atual

                else:
                    preco_medio_anterior = acumulado / somatorio
                    print('Se tipo_anterior =', tipo_anterior, 'Preçomédioanterior = ', acumulado, '/', somatorio)

                    preco_medio_atual = (acumulado / somatorio)

                    item.pmedio = preco_medio_atual

                tipo_anterior = item.invoice.transaction_kind

            quantidade_anterior = item.quantity


            item.saldo = somatorio #Quantidade de estoque na data de emissãodo documento
            item.acumulado_estoque = acumulado # Somatório dos estoques para compor a média no campo item.pmedio

            estoques[item.title] = somatorio #Armazenando os valores do estoque
            acumulados_estoques[item.title] = acumulado #Armazenando os valores do estoque somente de entradas

            item.esant = acumulado_anterior

            item.medio_ant = preco_medio_anterior
            item.apuracao = somatorio * (item.unit_price-preco_medio_atual)

    context = {'items': items}
    print(context)
    return render(request, 'checkout/item_list.html', context)

