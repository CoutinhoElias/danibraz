# from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Person(models.Model):
    name = models.CharField('Nome',max_length=100)
    birthday = models.DateField('Aniversário')
    address1 = models.CharField('Endereço 1',max_length=100)
    purchase_limit = models.DecimalField('Limite de compra',max_digits=15, decimal_places=2)


    class Meta:
        verbose_name_plural = 'pessoas'
        verbose_name = 'pessoa'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return u'/cadastro/pessoas'


class Address(models.Model):
    KINDS = (
        ('P', 'PRINCIPAL'),
        ('C', 'COBRANÇA'),
        ('E', 'ENTREGA'),
    )
    person = models.ForeignKey('persons.Person', related_name='address')
    kynd = models.CharField('Tipo', max_length=1, choices=KINDS)
    public_place = models.CharField('Logradouro',max_length=150)
    number = models.CharField('Número',max_length=150)
    city = models.CharField('Cidade',max_length=150)
    state = models.CharField('Estado',max_length=150)
    zipcode = models.CharField('Cep',max_length=10)
    country = models.CharField('País',max_length=150)
    neighborhood = models.CharField('Bairro',max_length=50)

    class Meta:
        verbose_name_plural = 'endereços'
        verbose_name = 'endereço'
        unique_together = ('person', 'kynd')

    def __str__(self):
        return self.public_place



class Client(Person):
    compra_sempre = models.BooleanField('Compra Sempre',default=False)

    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return u'cadastro/clientes/editar/%d' % self.id

    def get_absolute_url(self):
        return reverse('persons:clients_editar', args=[str(self.id)])



    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'



class Employee(Person):
    ctps = models.CharField('Carteira de Trabalho',max_length=25)
    salary = models.DecimalField('Salário',max_digits=15, decimal_places=2)


    def save(self, *args, **kwargs):
        # self.operacao = CONTA_OPERACAO_DEBITO
        super(Employee, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

"""---------------------------------------------------------------"""


class Author(models.Model):
    name = models.CharField(max_length=100)
    title_author = models.CharField('Titulo Autor', max_length=100)

class Book(models.Model):
    author = models.ForeignKey('Author')
    title1 = models.CharField('Titulo 1', max_length=100)
    title2 = models.CharField('Titulo 2', max_length=100)
    title3 = models.CharField('Titulo 3', max_length=100)