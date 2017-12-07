from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, render_to_response

# Create your views here.
from django.template import RequestContext
from django.urls import reverse_lazy
<<<<<<< HEAD
from django.views.generic import FormView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSet, NamedFormsetsMixin

from danibraz.checkout.forms import InvoiceForm, ItemInvoiceFormSet, \
    ItemInvoiceUpdateFormSet, ItemForm, ItemFormSet, InvoiceFormB
=======
from django.views.generic import ListView, CreateView, FormView, UpdateView
from extra_views import CreateWithInlinesView, InlineFormSet, NamedFormsetsMixin

from danibraz.checkout.forms import LancamentoForm, LancamentoItemFormSet, InvoiceForm, ItemInvoiceFormSet, \
    ItemInvoiceUpdateFormSet, ItemForm
>>>>>>> 4602188e886e7338a701ed8cec6e40a7379d83c1
from danibraz.checkout.models import Invoice, Item


#///////////////////////////////////////////////////////////////////////////////////
#AJUSTAR DELETE E EDIT
def invoices_create(request):
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

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = ItemFormSet(request.POST, instance=invoice)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()

            return redirect('/invoices/')
    else:
        form = InvoiceForm(instance=invoice)
        formset = ItemFormSet(instance=invoice)

<<<<<<< HEAD
    forms = [formset.empty_form] + formset.forms
    context = {'form': form, 'formset': formset, 'forms': forms}
    return render(request, 'invoices_edit.html', context)

def invoices_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice.delete()
        return redirect('/invoices/')

    return render(request, 'invoices_delete.html', {'invoice': invoice})

#///////////////////////////////////////////////////////////////////////////////////
=======
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




>>>>>>> 4602188e886e7338a701ed8cec6e40a7379d83c1
class InvoiceUpdateView(SuccessMessageMixin, UpdateView):
    model = Invoice
    form_class = InvoiceFormB
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


def invoice_list(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    print(context)
    return render(request, 'checkout/invoice_list.html', context)
