# Create your views here.
import logging
from django.core.checks import messages
from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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


def upload_xls(request):
    data = {}

    if "GET" == request.method:
        return render(request, "bolsa/import_form.html", data)
    # if not GET, then proceed
    try:
        xls_file = request.FILES["xls_file"]
        if not xls_file.name.endswith('.xls'):
            messages.error(request, 'File is not xls type')
            return HttpResponseRedirect(reverse("myapp:upload_xls"))
        # if file is too large, return
        if xls_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (xls_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("myapp:upload_xls"))

        file_data = xls_file.read().decode("utf-8")

        lines = file_data.split("\n")

        # from danibraz.bolsa.models import PlanoDeContas
        # import xlrd
        workbook = xlrd.open_workbook(file_data)
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

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect('bolsa/planodecontas/listar/')