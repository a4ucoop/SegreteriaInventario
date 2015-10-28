from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db import connection

def prova(request):
    """
    """

    cursor = connection.cursor()

    cursor.execute("select V_IE_CO_INVENTARIO_BENI.DS_BENE, V_IE_CO_INVENTARIO_BENI.ID_INVENTARIO_BENI, V_IE_CO_MOVIMENTI_BENE.DT_REGISTRAZIONE_BUONO, V_IE_CO_INVENTARIO_BENI.VALORE_CONVENZIONALE, V_IE_CO_INVENTARIO_BENI.CD_UBICAZIONE, V_IE_CO_INVENTARIO_BENI.DT_INI_AMMORTAMENTO from V_IE_CO_MOVIMENTI_BENE inner join V_IE_CO_INVENTARIO_BENI on V_IE_CO_MOVIMENTI_BENE.ID_INVENTARIO_BENI = V_IE_CO_INVENTARIO_BENI.ID_INVENTARIO_BENI where V_IE_CO_INVENTARIO_BENI.ID_INVENTARIO_BENI = V_IE_CO_MOVIMENTI_BENE.ID_INVENTARIO_BENI and V_IE_CO_INVENTARIO_BENI.CD_UBICAZIONE='UBI.AMMIN_036' order by V_IE_CO_INVENTARIO_BENI.VALORE_CONVENZIONALE DESC")
    
    #cursor.execute("select * from V_IE_CO_MOVIMENTI_BENE where rownum<20")
    rows = cursor.fetchall()

    context = {'rows': rows}
    
    return render (request,'prova/prova.html',context)
