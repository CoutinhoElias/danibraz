from django.contrib import admin

# Register your models here.
from danibraz.bolsa.models import Lancamento


class LancamentoModelAdmin(admin.ModelAdmin):
    pass
    list_display = ('data','papel', 'operacao', 'total_cust')

admin.site.register(Lancamento, LancamentoModelAdmin)