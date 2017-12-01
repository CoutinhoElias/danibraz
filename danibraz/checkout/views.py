from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSet, NamedFormsetsMixin

from danibraz.checkout.forms import LancamentoForm, LancamentoItemFormSet, InvoiceForm, ItemInvoiceFormSet, \
    ItemInvoiceUpdateFormSet, ItemForm
from danibraz.checkout.models import Invoice, Item


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
    success_message = 'A nota foi criada corretamente.'

    def get_context_data(self, **kwargs):
        context = super(InvoiceFormView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ItemInvoiceFormSet(self.request.POST, prefix='items')
        else:
            context['formset'] = ItemInvoiceFormSet(prefix='items')
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        total = 0
        valid = True
        if formset.is_valid():
            invoice = form.save(commit=False)
            invoice.total = 0
            invoice.save()
            for item_form in formset.forms:
                if item_form.is_valid():
                    item = item_form.save(commit=False)
                    item.invoice = invoice
                    item.save()
                    total += item.quantity * item.unit_price
                    invoice.total = total
                    invoice.save()
                else:
                    valid = False
            if valid:
                return super(InvoiceFormView, self).form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            print('O form não é valido!')
            return self.render_to_response(self.get_context_data(form=form))


class FormActionViewMixin(object):
    form_action = None

    def get_form_action(self):
        if not self.form_action:
            raise ImproperlyConfigured(
                "%(cls)s is missing a 'form_action'. Define "
                "%(cls)s.form_action, or override "
                "%(cls)s.get_form_action()." % {
                    'cls': self.__class__.__name__
                }
            )
        return self.form_action

    def get_context_data(self, **kwargs):
        context = super(FormActionViewMixin, self).get_context_data(**kwargs)
        context['form_action'] = self.get_form_action()
        return context


class ItemInvoiceInlineFormSet(InlineFormSet):
    model = Item
    form_class = ItemForm
    min_num = 1
    max_num = 16
    validate_min = True
    validate_max = True
    extra = 2
    can_delete = False
    items = 'items'


class InvoiceCreateView(SuccessMessageMixin, FormActionViewMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = Invoice
    # fields = ['assistido']
    form_class = InvoiceForm
    template_name = 'checkout/invoice_form2.html'
    inlines = [
        ItemInvoiceInlineFormSet,
    ]
    inlines_names = [
        'iteminvoice_inline'
    ]

    def get_form_action(self):
        kwargs = {

        }
        return reverse_lazy('checkout:invoice_add2', kwargs=kwargs)

    def get_form_kwargs(self):
        kwargs = super(InvoiceCreateView, self).get_form_kwargs()
        kwargs['prefix'] = 'invoice'
        return kwargs

    def get_context_data(self, **kwargs):
        contexto = super(InvoiceCreateView, self).get_context_data(**kwargs)
        return contexto

    # repare que esse metodo é diferente "forms_valid" com "s" e não form_valid
    def forms_valid(self, form, inlines):
        invoice = form.save(commit=False)
        total = 0
        for inline in inlines:
            for item_form in inline.forms:
                item = item_form.save(commit=False)
                total = total + (item.quantity * item.unit_price)

        invoice.total = total
        # save sera chamado em:
        return super(InvoiceCreateView, self).forms_valid(form, inlines)

    def get_initial(self):
        initial = super(InvoiceCreateView, self).get_initial()

        initial.update(
            {
            }
        )
        return initial

    def get_success_url(self):
        url = reverse_lazy('checkout:invoice_add2')
        return url




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