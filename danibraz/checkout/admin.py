from django.contrib import admin

# Register your models here.
from danibraz.checkout.models import Item, Invoice, Papel, Transaction, Product


# class LancamentoItemInline(admin.TabularInline):
#     model = LancamentoItem
#     extra = 1
#
# class LancamentoModelAdmin(admin.ModelAdmin):
#     inlines = [LancamentoItemInline]



# admin.site.register(LancamentoItem)
# admin.site.register(Lancamento, LancamentoModelAdmin)


admin.site.register(Papel)


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

class InvoiceModelAdmin(admin.ModelAdmin):
    readonly_fields = ['total_prop']
    inlines = [ItemInline]



admin.site.register(Item)
admin.site.register(Invoice, InvoiceModelAdmin)


class TransactionModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'quantity', 'transaction_kind', 'date_transaction')

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')

admin.site.register(Product, ProductModelAdmin)
admin.site.register(Transaction, TransactionModelAdmin)