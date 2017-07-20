from material.admin.base import Inline
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

from danibraz.persons.forms import ClientsForm, EmployeeForm


def clients(request):
    if request.method == 'POST':
        form = ClientsForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/reserva/listagem/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            print(form)
            return render(request, 'persons/person.html', {'form':form})
    else:
        context = {'form': ClientsForm()}
        return render(request, 'persons/person.html', context)

# def scheduling_edit(request, id_booking):
#     booking = Booking.objects.get(id=id_booking)
#     if request.method == 'GET':
#         form = BookingsForm(instance=booking)
#     else:
#         form = BookingsForm(request.POST, instance=booking)
#         if form.is_valid():
#             new = form.save(commit=False)
#             new.save()
#             form.save_m2m()
#         return HttpResponseRedirect('/reserva/listagem/')
#     return render(request, 'bookings/scheduling_form.html', {'form': form})


def employees(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            print('<<<<==== FORM VALIDO ====>>>>')
            new = form.save(commit=False)
            new.save()
            form.save_m2m()

            return HttpResponseRedirect('/reserva/listagem/')
        else:
            print('<<<<==== AVISO DE FORMULARIO INVALIDO ====>>>>')
            return render(request, 'persons/person.html', {'form':form})
    else:
        context = {'form': EmployeeForm()}
        return render(request, 'persons/person.html', context)