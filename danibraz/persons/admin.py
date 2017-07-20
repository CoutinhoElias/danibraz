from django.contrib import admin

# Register your models here.

from danibraz.persons.models import Client, Employee, Address, Person


class AdressInline(admin.TabularInline):
     model = Address
     extra = 1

class PersonModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('name', 'birthday', 'address1', 'purchase_limit')

admin.site.register(Person, PersonModelAdmin)


class ClientModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('name', 'birthday', 'address1', 'purchase_limit', 'compra_sempre')

admin.site.register(Client, ClientModelAdmin)

class EmployeeModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('name', 'birthday', 'address1', 'purchase_limit', 'ctps', 'salary')

admin.site.register(Employee, EmployeeModelAdmin)


# ---------------------------------------------------
#
# # class AdressInline(admin.TabularInline):
# #     model = Address
#
# class PersonModelAdmin(admin.ModelAdmin):
#     pass
#     # inlines = [AdressInline]
#
# admin.site.register(Person, PersonModelAdmin)
#
#
# class ClientModelAdmin(admin.ModelAdmin):
#     pass
#     # inlines = [AdressInline]
#
# admin.site.register(Client, ClientModelAdmin)
#
# class EmployeeModelAdmin(admin.ModelAdmin):
#     pass
#     # inlines = [AdressInline]
#
# admin.site.register(Employee, EmployeeModelAdmin)
#
# from danibraz.persons.models import Person, Address, Client, Poll
#
#
# class AddressInline(admin.TabularInline):
#     model = Address
#
#
# class PersonModelAdmin(admin.ModelAdmin):
#     inlines = [AddressInline]
#
#     class Meta:
#         model = Person
#
#         # list_display = ('name', 'birthday', 'address1', 'purchase_limit')
#         # inlines = [AddressInline]

