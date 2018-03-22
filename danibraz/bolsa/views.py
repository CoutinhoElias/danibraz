# Create your views here.
from django.http import HttpResponse, request
from django.shortcuts import render
from .admin import PlanoDeContasResource
from danibraz.bolsa.models import PlanoDeContas


import xlrd


def export(request):
    planoDeContas_resource = PlanoDeContasResource()
    dataset = planoDeContas_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response



def importaPlanilha(request):
    # from danibraz.bolsa.models import PlanoDeContas
    # import xlrd
    workbook = xlrd.open_workbook("/home/eliaspai/Área de Trabalho/Plano de Contas.xls")
    #workbook = xlrd.open_workbook("/home/eliaspai/Área de Trabalho/MODELO_PLANO_DE_CONTAS_PARA_IMPORTAR.xls")

    worksheet = workbook.sheet_by_name("Plan1")

    lista = []

    print(worksheet.nrows)
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