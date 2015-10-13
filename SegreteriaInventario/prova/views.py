from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db import connection

def prova(request):
    """
    """

    cursor = connection.cursor()

    #cursor.execute("select * from V_IE_CO_MOVIMENTI_BENE inner join V_IE_CO_INVENTARIO_BENI on V_IE_CO_MOVIMENTI_BENE.ID_INVENTARIO_BENI = V_IE_CO_INVENTARIO_BENI.ID_INVENTARIO_BENI where V_IE_CO_INVENTARIO_BENI.ID_INVENTARIO_BENI = 44")
    cursor.execute("select * from V_IE_CO_MOVIMENTI_BENE where rownum<20")
    rows = cursor.fetchall()

    context = {'rows': rows}
    
    return render (request,'prova/prova.html',context)
