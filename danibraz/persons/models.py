# from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    # class Meta:
    #     abstract = True

    name = models.CharField('Nome',max_length=100)
    birthday = models.DateField('Aniversário')
    address1 = models.CharField('Endereço 1',max_length=100)
    purchase_limit = models.DecimalField('Limite de compra',max_digits=15, decimal_places=2)


    class Meta:
        verbose_name_plural = 'pessoas'
        verbose_name = 'pessoa'

    def __str__(self):
        return self.name

    def get_child(self):
        if hasattr(self, 'client'):
            return self.client
        elif hasattr(self, 'employee'):
            return self.employee
        else:
            return None

    def get_type(self):
        if hasattr(self, 'client'):
            return 'client'
        elif hasattr(self, 'employee'):
            return 'employee'
        else:
            return None


class Address(models.Model):
    KINDS = (
        ('P', 'PRINCIPAL'),
        ('C', 'COBRANÇA'),
        ('E', 'ENTREGA'),
    )
    person = models.ForeignKey('Person')
    kynd = models.CharField('Tipo', max_length=1, choices=KINDS)
    public_place = models.CharField('Logradouro',max_length=150)
    number = models.CharField('Número',max_length=150)
    city = models.CharField('Cidade',max_length=150)
    state = models.CharField('Estado',max_length=150)
    zipcode = models.CharField('Cep',max_length=10)
    country = models.CharField('País',max_length=150)
    phone = models.CharField('Fone',max_length=50)

    class Meta:
        verbose_name_plural = 'endereços'
        verbose_name = 'endereço'

    def __str__(self):
        return self.public_place



class Client(Person):
    compra_sempre = models.BooleanField('Compra Sempre',default=False)

    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)

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
