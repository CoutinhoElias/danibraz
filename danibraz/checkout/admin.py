from django.contrib import admin

# Register your models here.
from danibraz.checkout.models import Lancamento, LancamentoItem


class LancamentoItemInline(admin.TabularInline):
    model = LancamentoItem
    extra = 1

class LancamentoModelAdmin(admin.ModelAdmin):
    inlines = [LancamentoItemInline]



admin.site.register(LancamentoItem)
admin.site.register(Lancamento, LancamentoModelAdmin)