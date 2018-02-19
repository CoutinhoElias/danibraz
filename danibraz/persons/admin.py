from django.contrib import admin

# Register your models here.

from danibraz.persons.models import Client, Employee, Address, Person


class AdressInline(admin.TabularInline):
     model = Address
     extra = 1

class PersonModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('pk','name', 'birthday', 'observation', 'purchase_limit')

admin.site.register(Person, PersonModelAdmin)


class ClientModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('pk','name', 'birthday', 'observation', 'purchase_limit', 'compra_sempre')

admin.site.register(Client, ClientModelAdmin)

class EmployeeModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('name', 'birthday', 'observation', 'purchase_limit', 'ctps', 'salary')

admin.site.register(Employee, EmployeeModelAdmin)
