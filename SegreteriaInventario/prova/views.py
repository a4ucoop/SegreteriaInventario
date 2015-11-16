from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db import connection
from django import template

# prende il cursore che ha eseguito la query, estrae i risultati sotto
# forma di dizionario che ha come chiave il nome del campo
def rows_to_dict_list(cursor):
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in cursor]

def prova(request):

    cursor = connection.cursor()

    cursor.execute(
    	"SELECT \
	    	INV.ID_INVENTARIO_BENI,\
	    	INV.DS_BENE,\
	    	MOV.DT_REGISTRAZIONE_BUONO,\
	    	INV.VALORE_CONVENZIONALE,\
	    	SPA.DS_SPAZIO,\
	    	INV.DT_INI_AMMORTAMENTO\
    	FROM\
    		((V_IE_CO_MOVIMENTI_BENE MOV INNER JOIN V_IE_CO_INVENTARIO_BENI INV\
    		ON MOV.ID_INVENTARIO_BENI = INV.ID_INVENTARIO_BENI) INNER JOIN\
    		V_IE_AC_SPAZI SPA ON INV.CD_UBICAZIONE = SPA.CD_SPAZIO)\
    	WHERE\
    		rownum < 20\
    	ORDER BY\
    		INV.VALORE_CONVENZIONALE DESC"
    	)
    
    rows = rows_to_dict_list(cursor)

    context = {'rows': rows}
    
    return render (request,'prova/prova.html',context)

register = template.Library()

@register.filter
def qr(value,size="150x150"):
    """
        Usage:
        <img src="{{object.code|qr:"120x130"}}" />
    """
    return "http://chart.apis.google.com/chart?chs=%s&cht=qr&chl=%s&choe=UTF-8&chld=H|0" % (size, value)
