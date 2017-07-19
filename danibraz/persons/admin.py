from django.contrib import admin

# Register your models here.

from danibraz.persons.models import Client, Employee, Person#, Address


# class AdressInline(admin.TabularInline):
#     model = Address

class PersonModelAdmin(admin.ModelAdmin):
    pass
    # inlines = [AdressInline]

admin.site.register(Person, PersonModelAdmin)


class ClientModelAdmin(admin.ModelAdmin):
    pass
    # inlines = [AdressInline]

admin.site.register(Client, ClientModelAdmin)

class EmployeeModelAdmin(admin.ModelAdmin):
    pass
    # inlines = [AdressInline]

admin.site.register(Employee, EmployeeModelAdmin)

