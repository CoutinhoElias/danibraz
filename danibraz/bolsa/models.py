from django.db import models
#DATA-PAPEL-OP(COMPRA.VENDA,DIVIDENDOS,SPLIT), QTD, CUSTO TOTAL(CORRETAGEM+IMPOSTOS)
# Create your models here.
class Lancamento(models.Model):
    data = models.DateField('Data')
    papel = models.CharField('Papel',max_length=100)
    operacao = models.CharField('Operação',max_length=100)
    total_cust = models.DecimalField('Custo Total',max_digits=15, decimal_places=2)


    class Meta:
        verbose_name_plural = 'lançamentos'
        verbose_name = 'lançamento'

    def __str__(self):
        return self.papel