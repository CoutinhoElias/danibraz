from django.contrib import admin
from django_bulk_update.helper import bulk_update

# Register your models here.
from danibraz.bolsa.models import PlanoDeContas, Lancamento, CustoCblc, CustoBovespa, CustoCorretagem


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


from import_export import resources
from .models import PlanoDeContas

class PlanoDeContasResource(resources.ModelResource):

    class Meta:
        model = PlanoDeContas


from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(PlanoDeContas)
class PlanoDeContasAdmin(ImportExportModelAdmin):
    list_display = ('classification', 'new_classification','name', 'reduced_account', 'sn', 'n', 'account_type')

    actions = ['remove_charactere', 'include_charactere']


    def remove_charactere(self, request, queryset_planodecontas):

        queryset_planodecontas = PlanoDeContas.objects.all()

        # limpa os dados
        for planodecontas_obj in queryset_planodecontas:
            dado_a_limpar = planodecontas_obj.new_classification
            dado_limpo = dado_a_limpar.replace("-", "").replace(".", "")
            planodecontas_obj.new_classification = dado_limpo

        bulk_update(queryset_planodecontas, update_fields=['new_classification'], batch_size=5000)

    def include_charactere(self, request, queryset):
        import re


        # dados = [
        #     dict(
        #         new_classification=queryset_planodecontas.new_classification) for queryset_planodecontas in PlanoDeContas.objects.all()
        #     # '1', '101', '10101',
        #     # '1010110', '101011010', '10101101010',
        #     # '1010110101000015', '1.01.01.10.10.10.0001-6', '1.0101.10.10.10.0001-7',
        #     # '1.01.01.10.10.10.0002-1', '1.01.0110.10.10.0002-2', '1.01.01.10.10.1000023',
        # ]
        padrao = re.compile('(\d)(?:\.?(\d{2})(?:\.?(\d{2})(?:\.?(\d{2})(?:\.?(\d{2})(?:\.?(\d{2})(?:\.?(\d{4})-?(\d))?)?)?)?)?)?')

        def formatar(dado):
            res = padrao.search(dado)
            if res:
                res = tuple(filter(lambda v: v is not None, res.groups()))
                if len(res) > 6:
                    return '.'.join(res[:6]) + '.' + '-'.join(res[6:])
                return '.'.join(res[:6])

        dados = []
        for plano in PlanoDeContas.objects.all():
            plano.new_classification = formatar(plano.new_classification)
            dados.append(plano)

        bulk_update(dados)