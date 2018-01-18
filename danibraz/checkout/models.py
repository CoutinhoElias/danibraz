from datetime import date
from time import strptime

from django.core.exceptions import ValidationError
from django.db import models
from django.core.urlresolvers import reverse

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
TRANSACTION_KIND = (
    ("in", "Entrada"),
    ("out", "Saida"),
    ("eaj", "Entrada de Ajuste"),
    ("saj", "Saída de Ajuste")
)

class Papel(models.Model):
    symbol = models.CharField('Papel', max_length=100, choices=PAPEL_CHOICES)
    stock = models.IntegerField('Estoque')
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    class Meta:
        verbose_name = 'Papel'
        verbose_name_plural = 'Papeis'
        
    def stock_avaliable(self):
        itens_nota = Item.objects.select_related('title').all().order_by("created")
        total_avaliable = 0

        for transaction in itens_nota:
            if transaction.invoice.transaction_kind == 'in' or transaction.invoice.transaction_kind == 'eaj':
                total_avaliable += transaction.quantity
            else:
                total_avaliable -= transaction.quantity

        return total_avaliable


    def __unicode__(self):
        return "Produto {self.name} possuí {self.stock_avaliable()} em estoque."
    
    def __str__(self):
        return self.symbol

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.original_quantity = Item.quantity


class Invoice(models.Model):
    customer = models.ForeignKey('persons.Client')
    emissao = models.DateField('emissao')
    total = models.IntegerField('Total')
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    transaction_kind = models.CharField('Tipo Movimento', max_length=4, choices=TRANSACTION_KIND)

    def get_absolute_url(self):
        return reverse('checkout:invoice_edit', args=(self.pk,))



class Item(models.Model):
    invoice = models.ForeignKey('checkout.Invoice', related_name='item')
    title = models.ForeignKey('checkout.Papel')
    quantity = models.PositiveSmallIntegerField('quantidade')
    unit_price = models.DecimalField('unit price', max_digits=10, decimal_places=2)
    other_costs = models.DecimalField('other costs', max_digits=10, decimal_places=2)
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    @property
    def total(self):
        return (self.quantity * self.unit_price) + self.other_costs

    @property
    def stock(self):
        return self.title.stock

    class Meta:
        verbose_name = 'Item da Nota'
        verbose_name_plural = 'Itens da Nota'
        #unique_together = (('invoice', 'title'),)

    # def clean(self, *args, **kwargs):
    #     try:
    #         qtd = Item.objects.get(pk=self.pk)
    #         #print('Estoque: ', self.title.stock, ', Quantidade nova: ', self.quantity, ', Quantidade antiga: ',
    #         #      qtd.quantity, ', Id da nota: ', self.pk)
    #
    #         if self.title.stock < (qtd.quantity - self.quantity):
    #             raise ValidationError({'quantity': (u"Quantidade está maior que estoque!")})
    #         super(Item, self).clean(*args, **kwargs)
    #
    #     except Item.DoesNotExist:
    #         if self.title.stock < self.quantity:
    #             raise ValidationError({'quantity': (u"Quantidade está maior que estoque!")})
    #         super(Item, self).clean(*args, **kwargs)


def post_save_item(sender, instance, created,  **kwargs):
    if created:
        if instance.invoice.transaction_kind == 'in' or instance.invoice.transaction_kind == 'eaj':
            instance.title.stock += instance.quantity
            instance.title.save()
        else:
            instance.title.stock -= instance.quantity
            instance.title.save()
    else:
        instance.title.stock -= instance.title.stock
        instance.title.stock += instance.title.stock_avaliable()
        instance.title.save()


    # try:
    #     qtd = Item.objects.get(pk=instance.pk)
    # 
    #     instance.title.stock -= (instance.quantity - qtd.quantity)
    #     instance.title.save()
    # 
    # except Item.DoesNotExist:
    #     instance.title.stock -= instance.quantity
    #     instance.title.save()


models.signals.post_save.connect(
    post_save_item, sender=Item, dispatch_uid='post_save_item'
)





class Product(models.Model):
    name = models.CharField(max_length=100)
    #deleted = models.BooleanField(default=False)

    def stock_avaliable(self):
        transactions = self.transactions.all().order_by("date_transaction")
        total_avaliable = 0

        for transaction in transactions:
            if transaction.transaction_kind == 'in' or transaction.transaction_kind == 'eaj':
                total_avaliable += transaction.quantity
            else:
                total_avaliable -= transaction.quantity

        return total_avaliable

    def __unicode__(self):
        return "Produto {self.name} possuí {self.stock_avaliable()} em estoque."

    def __str__(self):
        return self.name


class Transaction(models.Model):
    quantity = models.PositiveIntegerField()
    transaction_kind = models.CharField(max_length=4, choices=TRANSACTION_KIND)
    date_transaction = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, related_name='transactions')

    def historico_vendas(self, product, **extra_filter):
        pass

    def historico_entradas(self, product, **extra_filter):
        # transactions
        # estrutura para montar algo \o/
        pass

    def __unicode__(self):
        trans_kind = "Entrada"
        return "{trans_kind} de {self.quantity} unidades do produto {self.product.name} no dia {self.date_transaction}."

    def __str__(self):
        return self.transaction_kind


# # Passo 1
# papel = Product(name="Folha de Papel")
# papel.save()
# compra_papel = Transaction(quantity=300, transaction_kind="in", product=papel)
# compra_papel.save()
# papel.stock_avaliable() # 300
# # Fim do Passo 1
#
# # Passo 2
# papel = Product.objects.get(name="Folha de Papel")
# venda_papel = Transaction(quantity=100, transaction_kind="out", product=papel)
# venda_papel.save()
# papel.stock_avaliable() # 200
# # Fim do Passo 2
#
# # Edit produto
# pacote_papel = Product.objects.get(name="Folha de Papel")
# pacote_papel.name = "Pacote de 500 folhas de papel"
# pacote_papel.stock_avaliable() # 200
# pacote_papel.save()
# pacote_papel.stock_avaliable() # 200
# ajuste = Transaction(quantity=190, transaction_kind="saj", product=pacote_papel)
# ajuste.save()
# pacote_papel.stock_avaliable() # 10
# # Fim Edit


#MEU MODELO
# 1 - IMPORTA OS MODELOS
#from danibraz.checkout.models import Product, Transaction

# 2 - CRIA UMPRODUTO
#Product.objects.create(name='Novo produto')

# 3 - FILTRA ESSEPRODUTO PARA USAR NO INSERT
#prod = Product.objects.all().[0]

# 4 - CRIA UMAMOVIMENTAÇÃO DEENTRADA OU SAÍDA
#Transaction.objects.create(quantity=190, transaction_kind="saj", product=prod)

# 5 - RETORNAO ESTOQUE ATUAL DO PRODUTO
#prod.stock_avaliable()
