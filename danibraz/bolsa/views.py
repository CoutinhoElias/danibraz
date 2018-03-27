# Create your views here.
import logging
from django.core.checks import messages
from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse

from danibraz.bolsa.forms import FileUploadForm
from .admin import PlanoDeContasResource
from danibraz.bolsa.models import PlanoDeContas


import xlrd


def export(request):
    planoDeContas_resource = PlanoDeContasResource()
    dataset = planoDeContas_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response





def upload_xls2(request):
    if request.method == 'POST': # If the form has been submitted...
        form = FileUploadForm(request.POST) # Um form com os dados de POST
        if form.is_valid(): # All validation rules pass
            # Processa os dados no form.cleaned_data
            # ...
            #csv_file = request.FILES["csv_file"]
            csv_file = request.FILES['csv_file']

            print(csv_file)
            
            return HttpResponseRedirect('/thanks/') # Redireciona depois do POST
    else:
        form = FileUploadForm() # Um formulário vazio

    return render_to_response('bolsa/import_form.html', {
        'form': form,
    })

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import FileUploadForm



# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['excelfile']:
#         myfile = request.FILES['excelfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, '/bolsa/importar/', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'bolsa/import_form.html')


def simple_upload(request):
    if request.method == 'POST' and request.FILES['excelfile']:
        myfile = request.FILES['excelfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        dir = fs.open(myfile.name, mode = 'rb' )
        print('-----------------------------------------------------')
        print('Diretório:  ', dir)
        print('myfile.name:  ',myfile.name)
        print('myfile:  ', myfile)
        print('FileSystemStorage:  ', fs)
        print('filename:  ', filename)
        print('uploaded_file_url:  ', uploaded_file_url)
        print('-----------------------------------------------------')
        importaPlanilha(dir)

        return HttpResponseRedirect('/bolsa/importar/')

    return render(request, 'bolsa/import_form.html')

def importaPlanilha(dir):
    fileDir = dir
    print(fileDir,'---------------------------')
    # from danibraz.bolsa.models import PlanoDeContas
    # import xlrd
                                   #/home/eliaspai/danibraz_err/danibraz/media/MODELO_PLANO_DE_CONTAS_PARA_IMPORTAR.xls
    #workbook = xlrd.open_workbook("/home/eliaspai/Área de Trabalho/Plano de Contas.xls")
    workbook = xlrd.open_workbook(dir)
    #workbook = xlrd.open_workbook("/home/eliaspai/Área de Trabalho/MODELO_PLANO_DE_CONTAS_PARA_IMPORTAR.xls")

    worksheet = workbook.sheet_by_name("Plan1")

    lista = []

    #print(worksheet.nrows)
    for r in range(1, worksheet.nrows):
        a = str(worksheet.cell(r, 0).value)

        if (a[len(a) - 2:] == '.0') or (len(a) > 0):
            classific = a[:len(a) - 2]
            #print(a[:len(a) - 2], '<---->','Tamanho: ', len(a))
        elif len(a) == 0:
            continue
        else:
            classific = a
            #print(str(worksheet.cell(r, 0).value))

        lista.append(
            PlanoDeContas(classification=str(worksheet.cell(r, 0).value),
                          new_classification=str(classific),
                          name=worksheet.cell(r, 2).value,
                          reduced_account=worksheet.cell(r, 3).value,

                          )
        )

    PlanoDeContas.objects.bulk_create(lista)

    planodecontas = PlanoDeContas.objects.all()
    context = {'planodecontas': planodecontas}
    return render(request, 'bolsa/bolsa_list.html', context)


def planodecontas_list(request):
    q = request.GET.get('search_box')
    print(request.GET)
    if q:
        print(q)
        planodecontas = PlanoDeContas.objects.filter(name__icontains=q)
    else:
        planodecontas = PlanoDeContas.objects.all()
    context = {'planodecontas': planodecontas}
    print(context)
    return render(request, 'bolsa/bolsa_list.html', context)


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            importaPlanilha(request.FILES['excelfile'])
            f = request.FILES['excelfile']
            print(f)
            return HttpResponseRedirect('/bolsa/importar/')
            #return excel.make_response(filehandle.get_sheet(), "csv")
    else:
        form = FileUploadForm()
    return render(request, 'bolsa/import_form.html', {'form': form})