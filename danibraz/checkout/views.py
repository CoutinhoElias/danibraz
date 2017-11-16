from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, UpdateView

from danibraz.checkout.forms import LancamentoForm, LancamentoItemFormSet, InvoiceForm, ItemInvoiceFormSet, \
    ItemInvoiceUpdateFormSet
from danibraz.checkout.models import Invoice


def lancamentos_create2(request):
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
    return render(request, 'checkout/lancamentos_edit_material_2.html', context)

#
# class ListadoCompras(ListView):
#     model = Compra
#     template_name = 'compras.html'
#     context_object_name = 'compras'
#
#
# class CrearCompra(CreateView):
#     pass

# def lancamentos(request):
#     if request.method == 'POST':
#
#         form = LancamentoForm(request.POST)
#
#         if form.is_valid():
#             print('<<<<==== FORM VALIDO ====>>>>')
#             new = form.save(commit=False)
#             new.save()
#             form.save_m2m()
#             return redirect(new)
#             #return HttpResponseRedirect('/reserva/listagem/')
#         else:
#             print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
#             print(form)
#             return render(request, 'checkout/lancamentos_edit_material.html', {'form':form})
#     else:
#         context = {'form': LancamentoForm()}
#         return render(request, 'checkout/lancamentos_edit_material.html', context)
#
#
# def lancamentos_edit(request, lancamento_id):
#     lancamento = get_object_or_404(Lancamento, pk=lancamento_id)
#     if request.method == 'POST':
#         form = LancamentoForm(request.POST, instance=lancamento)
#         if form.is_valid():
#             print('<<<<==== FORM VALIDO ====>>>>')
#             new = form.save(commit=False)
#             new.save()
#             form.save_m2m()
#             return HttpResponseRedirect('/lancamento/pedido/editar/'+lancamento_id, lancamento_id)
#         else:
#             print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
#             print(form)
#             return render(request, 'checkout/lancamentos_edit_material.html', {'form':form})
#     else:
#         print('Entrou em modo de edição do cliente '+lancamento_id)
#
#         request.session['lancamento_id'] = lancamento_id
#         print('A variável lancamento_id da session já possui o valor: '+request.session['lancamento_id'])
#         #return HttpResponseRedirect('/cadastro/clientes/listar/')
#         context = {'form': LancamentoForm(instance=lancamento)}
#         return render(request, 'checkout/lancamentos_edit_material.html', context)

class InvoiceFormView(SuccessMessageMixin, FormView):
    form_class = InvoiceForm
    template_name = 'checkout/invoice_form.html'
    success_url = reverse_lazy('checkout:invoice_add')
    #success_url = reverse_lazy('invoicing:invoice_list')
    success_message = 'The invoice was created correctly.'

    def get_context_data(self, **kwargs):
        context = super(InvoiceFormView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ItemInvoiceFormSet(self.request.POST, prefix='items')
        else:
            context['formset'] = ItemInvoiceFormSet(prefix='items')
        return context

    # Linha 38, ocampo invoice.total receberá oitem.quantity * item.unit_pryce
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        total = 0
        if formset.is_valid():
            invoice = form.save(commit=False)
            invoice.total = 0
            invoice.save()
            for item_form in formset.forms:
                item = item_form.save(commit=False)
                item.invoice = invoice
                item.save()
                total += item.quantity * item.unit_price
            invoice.total = total
            invoice.save()
            return super(InvoiceFormView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class InvoiceUpdateView(SuccessMessageMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'checkout/invoice_form.html'
    success_url = reverse_lazy('checkout:invoice_list')
    success_message = 'The invoice was edited correctly.'

    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        invoice = self.get_object()
        productos = invoice.nota.all()
        if self.request.POST:
            context['formset'] = ItemInvoiceUpdateFormSet(self.request.POST, self.request.FILES, prefix='items')
        else:
            context['formset'] = ItemInvoiceUpdateFormSet(queryset=productos, prefix='items')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        total = 0
        if formset.is_valid():
            invoice = form.save(commit=False)
            for item_form in formset.forms:
                item = item_form.save(commit=False)
                item.invoice = self.get_object()
                item.save()
                total += item.quantity * item.unit_price
            formset.save()
            invoice.total = total
            invoice.save()
            return super(InvoiceUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

# class InvoiceSingleTableView():
#     #table_class = InvoiceTable.....
#     queryset = Invoice.objects.all()
#     template_name = 'invoice_list.html'

def invoice_list(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    print(context)
    return render(request, 'checkout/invoice_list.html', context)


# def InvoiceUpdateView(request, invoice_id):
#     invoice_id = get_object_or_404(Invoice, pk=invoice_id)
#     if request.method == 'POST':
#         form = InvoiceForm(request.POST, invoice_id)
#         formset = ItemInvoiceUpdateFormSet(request.POST)
#
#         if form.is_valid() and formset.is_valid():
#             with transaction.atomic():
#                 item = form.save()
#                 formset.instance = item
#                 formset.save()
#
#             return redirect('/teams/')
#     else:
#         form = InvoiceForm()
#         formset = ItemInvoiceUpdateFormSet()
#
#     forms = [formset.empty_form] + formset.forms
#     context = {'form': form, 'formset': formset, 'forms': forms}
#     return render(request, 'checkout/invoice_form.html', context)