from django.contrib import admin

# Register your models here.
from danibraz.bolsa.models import Lancamento, CustoCblc, CustoBovespa, CustoCorretagem


class CustoCblcInline(admin.TabularInline):
    model = CustoCblc
    extra = 1

class CustoBovespaInline(admin.TabularInline):
    model = CustoBovespa
    extra = 1


class CustoCorretagemInline(admin.TabularInline):
    model = CustoCorretagem
    extra = 1

class LancamentoModelAdmin(admin.ModelAdmin):
    readonly_fields = ['custo_total', 'credito', 'debito']

    inlines = [
        CustoCblcInline, CustoBovespaInline, CustoCorretagemInline
    ]

    list_display = ('data','papel', 'operacao','quantidade', 'custo_total')


admin.site.register(Lancamento, LancamentoModelAdmin)


class PessoaModelAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('id','nomepessoa', 'tipologradouro','numero', 'bairro', 'cidade', 'estado')

    def get_form(self, request, obj=None, **kwargs):
        form = super(PessoaModelAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['username'].initial = request.user.pk
        return form