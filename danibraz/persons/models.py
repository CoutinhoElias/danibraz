# from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    # class Meta:
    #     abstract = True

    name = models.CharField(max_length=100)
    birthday = models.DateField()
    address = models.CharField(max_length=100)
    purchase_limit = models.DecimalField(max_digits=15, decimal_places=2)


class Client(Person):
    compra_sempre = models.BooleanField(default=False)
    # person = models.ForeignKey('persons.Person', verbose_name='Pessoa', related_name='Person')
    def save(self, *args, **kwargs):
        # self.operacao = CONTA_OPERACAO_DEBITO


        super(Client, self).save(*args, **kwargs)


class Employee(Person):
    ctps = models.CharField(max_length=25)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
