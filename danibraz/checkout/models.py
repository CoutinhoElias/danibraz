from django.core.exceptions import ValidationError
from django.db import models
from django.core.urlresolvers import reverse
from django.core.signals import request_finished

# Create your models here.
from django.db.models import Sum

OPERACAO_CHOICES = (
    ('C', 'COMPRA'),
    ('V', 'VENDA'),
    ('D', 'DIVIDENDOS'),
    ('S', 'SPLIT')
)


PAPEL_CHOICES = (
    ('ABEV3', 'AMBEV S/A'),
    ('BBAS3', 'BRASIL'),
    ('BBDC3', 'BRADESCO 3'),
    ('BBDC4', 'BRADESCO 4'),
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
    # papel = models.CharField('Papel',max_length=100, choices=PAPEL_CHOICES)
    # operacao = models.CharField('Operação',max_length=100, choices=OPERACAO_CHOICES)
    # quantidade = models.PositiveIntegerField('Quantidade', default=1)

    class Meta:
        verbose_name_plural = 'lançamentos'
        verbose_name = 'lançamento'

    def __str__(self):
        return str(self.data)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('checkout:lancamento_editar', args=[str(self.id)])


class LancamentoItem(models.Model):
    lancamento = models.ForeignKey('checkout.Lancamento', related_name='lancamento_item')
    symbol = models.CharField('Papel',max_length=100, choices=PAPEL_CHOICES)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do Lançamento'
        verbose_name_plural = 'Itens do Lancamento'

    def __str__(self):
        return '{} [{}]'.format(self.lancamento, self.quantity)


#----------------------------------------------------------------------------------
class Papel(models.Model):
    symbol = models.CharField('Papel', max_length=100, choices=PAPEL_CHOICES)
    stock = models.PositiveSmallIntegerField('Estoque')
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    class Meta:
        verbose_name = 'Papel'
        verbose_name_plural = 'Papeis'

    def __str__(self):
        return self.symbol


class Invoice(models.Model):
    customer = models.ForeignKey('persons.Client')
    emissao = models.DateField('emissao')
    total = models.IntegerField('Total')
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    def get_absolute_url(self):
        return reverse('checkout:invoice_edit', args=(self.pk,))

    # def get_absolute_url(self):
    #     return reverse('persons:clients_editar', args=[str(self.id)])

    @property
    def total_prop(self):
        return self.nota.all().aggregate(Sum('unit_price'))['unit_price__sum'] #+ self.custo_bovespa.all().aggregate(Sum('emolumentos'))['emolumentos__sum']



class Item(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='nota')
    title = models.ForeignKey('checkout.Papel')
    quantity = models.DecimalField('quantity', max_digits=10, decimal_places=3, default=1)
    unit_price = models.DecimalField('unit price', max_digits=10, decimal_places=2)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    class Meta:
        verbose_name = 'Item da Nota'
        verbose_name_plural = 'Itens da Nota'
        #unique_together = (('invoice', 'title'),)

def post_save_item(sender, instance, **kwargs):
    if instance.title.stock >= instance.quantity:
        instance.title.stock -= instance.quantity
        instance.title.save()
    else:
        # instance.title.stock = 0
        # instance.title.save()
        raise ValidationError('O valor do estoque ficará negativo, Não foi salvo')


models.signals.post_save.connect(
    post_save_item, sender=Item, dispatch_uid='post_save_item'
)