from django.contrib import admin

# Register your models here.

from danibraz.persons.models import Client, Employee, Address, Person, Author, Book


class AdressInline(admin.TabularInline):
     model = Address
     extra = 1

class PersonModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('pk','name', 'birthday', 'address1', 'purchase_limit')

admin.site.register(Person, PersonModelAdmin)


class ClientModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('pk','name', 'birthday', 'address1', 'purchase_limit', 'compra_sempre')

admin.site.register(Client, ClientModelAdmin)

class EmployeeModelAdmin(admin.ModelAdmin):
    pass
    inlines = [AdressInline]
    list_display = ('name', 'birthday', 'address1', 'purchase_limit', 'ctps', 'salary')

admin.site.register(Employee, EmployeeModelAdmin)


"""----------------------------------------------------------------------------"""


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


class AuthorModelAdmin(admin.ModelAdmin):
    pass
    inlines = [BookInline]
    list_display = ['name']


admin.site.register(Author, AuthorModelAdmin)

