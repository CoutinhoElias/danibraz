from django.db import models
#DATA-PAPEL-OP(COMPRA.VENDA,DIVIDENDOS,SPLIT), QTD, CUSTO TOTAL(CORRETAGEM+IMPOSTOS)
# Create your models here.
# Agrupar itenspor nota
# Casas decimaispara o valor= 4  okokokok
# Lançar os custos em um inline e o sistema aglutinae leva para o movimento. okokokok/2


OPERACAO_CHOICES = (
    ('C', 'COMPRA'),
    ('V', 'VENDA'),
    ('D', 'DIVIDENDOS'),
    ('S', 'SPLIT')
)

class Lancamento(models.Model):
    data = models.DateField('Data')
    papel = models.CharField('Papel',max_length=100)
    operacao = models.CharField('Operação',max_length=100, choices=OPERACAO_CHOICES)
    quantidade = models.IntegerField('Quantidade')
    total_cust = models.DecimalField('Custo Total',max_digits=15, decimal_places=4)

    def total_cblc(self):
        aggregate_queryset = self.custo_cblc.aggregate(
            total=models.Sum(
                models.F('valor_liquido') + models.F('taxa_liquidacao'), + models.F('taxa_registro'),
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']

    class Meta:
        verbose_name_plural = 'lançamentos'
        verbose_name = 'lançamento'

    def __str__(self):
        return self.papel


class CustoCblc(models.Model):
    lancamento = models.ForeignKey('bolsa.Lancamento', related_name='custo_cblc')
    valor_liquido = models.DecimalField('Valor líquido das operações', max_digits=15, decimal_places=4)
    taxa_liquidacao = models.DecimalField('Taxa de liquidação', max_digits=15, decimal_places=4)
    taxa_registro = models.DecimalField('Taxa de registro', max_digits=15, decimal_places=4)


    class Meta:
        verbose_name_plural = 'Custos CBLC'
        verbose_name = 'Custo CBLC'


    # def __str__(self):
    #     return self.valor_liquido


class CustoBovespa(models.Model):
    lancamento = models.ForeignKey('bolsa.Lancamento', related_name='custo_bovespa')
    termo_opcoes = models.DecimalField('Taxa de termo/opções', max_digits=15, decimal_places=4)
    ana = models.DecimalField('Taxa de ANA', max_digits=15, decimal_places=4)
    emolumentos = models.DecimalField('Emolumentos', max_digits=15, decimal_places=4)


    class Meta:
        verbose_name_plural = 'Custos Bovespa/Soma'
        verbose_name = 'Custo Bovespa/Soma'


    # def __str__(self):
    #     return self.termo_opcoes


class CustoCorretagem(models.Model):
    lancamento = models.ForeignKey('bolsa.Lancamento', related_name='custo_corretagem')
    corretagem = models.DecimalField('Corretagem', max_digits=15, decimal_places=4)
    iss_pis_cofins = models.DecimalField('ISS / PIS / COFINS', max_digits=15, decimal_places=4)
    irrf_operacoes = models.DecimalField('I.R.R.F. s/ operações. Base R$ 0,00', max_digits=15, decimal_places=4)
    outras_bovespa = models.DecimalField('Outras Bovespa', max_digits=15, decimal_places=4)

    class Meta:
        verbose_name_plural = 'Corretagem / Despesas'
        verbose_name = 'Corretagem / Despesa'


    # def __str__(self):
    #     return self.corretagem