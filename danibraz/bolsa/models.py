from django.db import models
#DATA-PAPEL-OP(COMPRA.VENDA,DIVIDENDOS,SPLIT), QTD, CUSTO TOTAL(CORRETAGEM+IMPOSTOS)
# Create your models here.
# Agrupar itenspor nota
# Casas decimaispara o valor= 4  okokokok
# Lançar os custos em um inline e o sistema aglutinae leva para o movimento. okokokok/2
from django.db.models import Sum
from django.urls import reverse

OPERACAO_CHOICES = (
    ('C', 'COMPRA'),
    ('V', 'VENDA'),
    ('D', 'DIVIDENDOS'),
    ('S', 'SPLIT')
)


PAPEL_CHOICES = (
    ('ABEV3', 'AMBEV S/A'),
    ('BBAS3', 'BRASIL'),
    ('BBDC3', 'BRADESCO'),
    ('BBDC4', 'BRADESCO'),
    ('BBSE3', 'BBSEGURIDADE'),
    ('BRAP4', 'BRADESPAR'),
    ('BRFS3', 'BRF SA'),
    ('BRKM5', 'BRASKEM'),
    ('BRML3', 'BR MALLS PAR'),
    ('BVMF3', 'BMFBOVESPA'),
    ('CCRO3', 'CCR SA'),
    ('CIEL3', 'CIELO'),
    ('CMIG4', 'CEMIG'),
    ('CSAN3', 'COSAN'),
    ('CSNA3', 'SID NACIONAL'),
    ('ECOR3', 'ECORODOVIAS'),
    ('ELET3', 'ELETROBRAS'),
    ('EMBR3', 'EMBRAER'),
    ('EQTL3', 'EQUATORIAL'),
    ('ESTC3', 'ESTACIO PART'),
    ('FIBR3', 'FIBRIA'),
    ('GGBR4', 'GERDAU'),
    ('GOAU4', 'GERDAU MET'),
    ('HYPE3', 'HYPERMARCAS'),
    ('ITSA4', 'ITAUSA'),
    ('ITUB4', 'ITAUUNIBANCO'),
    ('JBSS3', 'JBS'),
    ('KLBN11', 'KLABIN S/A'),
    ('KROT3', 'KROTON'),
    ('LAME4', 'LOJAS AMERIC'),
    ('LREN3', 'LOJAS RENNER'),
    ('MRVE3', 'MRV'),
    ('MULT3', 'MULTIPLAN'),
    ('NATU3', 'NATURA'),
    ('PCAR4', 'P.ACUCAR-CBD'),
    ('PETR3', 'PETROBRAS'),
    ('PETR4', 'PETROBRAS'),
    ('QUAL3', 'QUALICORP'),
    ('RADL3', 'RAIADROGASIL'),
    ('RAIL3', 'RUMO S.A.'),
    ('RENT3', 'LOCALIZA'),
    ('SANB11', 'SANTANDER BR'),
    ('SBSP3', 'SABESP'),
    ('SUZB5', 'SUZANO PAPEL'),
    ('TAEE11', 'TAESA'),
    ('UGPA3', 'ULTRAPAR'),
    ('USIM5', 'USIMINAS'),
    ('VALE3', 'VALE'),
    ('VIVT4', 'TELEF BRASIL'),
    ('WEGE3', 'WEG')
)


class Lancamento(models.Model):
    data = models.DateField('Data')
    papel = models.CharField('Papel',max_length=100, choices=PAPEL_CHOICES)
    operacao = models.CharField('Operação',max_length=100, choices=OPERACAO_CHOICES)
    quantidade = models.IntegerField('Quantidade')

    @property
    def custo_total(self):
        return self.custo_cblc.all().aggregate(Sum('taxa_registro'))['taxa_registro__sum'] #+ self.custo_bovespa.all().aggregate(Sum('emolumentos'))['emolumentos__sum']

    @property
    def credito(self):
        return self.custo_cblc.filter(operacao ="C").aggregate(Sum('taxa_registro'))[
            'taxa_registro__sum']  # + self.custo_bovespa.all().aggregate(Sum('emolumentos'))['emolumentos__sum']

    @property
    def debito(self):
        return self.custo_cblc.filter(operacao__in=['D', 'V']).aggregate(Sum('taxa_registro'))[
            'taxa_registro__sum']

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
    operacao = models.CharField('Operação', max_length=100, choices=OPERACAO_CHOICES)


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

#0.00.00.00.00.00.0000-0
class PlanoDeContas(models.Model):
    classification = models.CharField('Classificação', primary_key=True, max_length=100)
    new_classification = models.CharField('Nova Classificação', max_length=100)
    name = models.CharField('Descrição', max_length=100)
    reduced_account = models.CharField('Conta reduzida', max_length=100)
    sn = models.CharField('SN', max_length=100)
    n = models.CharField('N', max_length=5)
    source = models.CharField('Origem', max_length=100)
    account_type = models.CharField('Tipo Conta', max_length=100)
    #
    # def get_absolute_url(self):
    #     return reverse('bolsa:invoice_edit', args=(self.pk,))