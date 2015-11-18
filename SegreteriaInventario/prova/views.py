from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db import connections
from django.db.models import Q
from django.shortcuts import redirect
from models import Item
import datetime
import json

def index(request):
	return render (request, 'prova/index.html')

# prende il cursore che ha eseguito la query, estrae i risultati sotto
# forma di dizionario che ha come chiave il nome del campo
def rows_to_dict_list(cursor):
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in cursor]



def showRemoteDB(request):

    cursor = connections['cineca'].cursor()

    cursor.execute(
    	"SELECT *\
    	FROM (\
	    	SELECT \
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
	    	ORDER BY\
	    		MOV.ID_INVENTARIO_BENI DESC\
    		)\
        WHERE\
            rownum < 100"
    	)

    rows = rows_to_dict_list(cursor)

    context = {'rows': rows}

    return render (request,'prova/provaRemote.html',context)



def showLocalDB(request):
    rows = Item.objects.using('default').all().order_by('-item_id')
    context ={'rows': rows}
    return render (request,'prova/provaLocal2.html',context)



def updateLocalDB(request):
    cursor = connections['cineca'].cursor()         # Cursor connessione Cineca
    cursorLocal = connections['default'].cursor()   # Cursor DB locale

    # Seleziona tutti i dati necessari dal DB remoto
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
            ORDER BY\
                MOV.ID_INVENTARIO_BENI DESC"
        )

    rows = rows_to_dict_list(cursor)

    # Scorre tutti i dati riga per riga
    for row in rows:
        # Per ogni riga vede se l'oggetto esiste gia' nel database
        try:
            item = Item.objects.get(item_id=row['ID_INVENTARIO_BENI'])

            # Se l'oggetto esiste i dati vengono aggiornati
            item.item_id = row['ID_INVENTARIO_BENI']
            item.description = row['DS_BENE']
            item.purchase_date = row['DT_REGISTRAZIONE_BUONO']
            item.price = row['VALORE_CONVENZIONALE']
            item.location = row['DS_SPAZIO']
            item.depreciation_starting_date = row['DT_INI_AMMORTAMENTO']

            # item = Item(None,item_id,description,purchase_date,price,location,depreciation_starting_date)
            item.save()
        except Item.DoesNotExist:
            # Se non esiste viene creato un nuovo oggetto
            item_id = row['ID_INVENTARIO_BENI']
            description = row['DS_BENE']
            purchase_date = row['DT_REGISTRAZIONE_BUONO']
            price = row['VALORE_CONVENZIONALE']
            location = row['DS_SPAZIO']
            depreciation_starting_date = row['DT_INI_AMMORTAMENTO']

            item = Item(None,item_id,description,purchase_date,price,location,depreciation_starting_date)
            item.save()

    return redirect ('showLocalDB')



def checkUpdate(request):
    cursor = connections['cineca'].cursor()         # Cursor connessione Cineca
    cursorLocal = connections['default'].cursor()   # Cursor DB locale

    # Ricava il massimo id da Cineca
    cursor.execute(
        "SELECT max(ID_INVENTARIO_BENI)\
         FROM V_IE_CO_INVENTARIO_BENI;"
    )

    # Ricava il massimo id dal DB locale
    cursorLocal.execute(
        "SELECT max(item_id)\
         FROM prova_item;"
    )

    maxRemoteID = cursor.fetchone()
    maxLocalID = cursorLocal.fetchone()

    # Se gli id sono diversi sono stati inseriti nuovi dati
    if maxRemoteID > maxLocalID:
        # Vengono ricavati tutti i nuovi items ovvero
        # quelli che hanno ID maggiore del massimo locale
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
                    INV.ID_INVENTARIO_BENI > %s\
                ORDER BY\
                    MOV.DT_REGISTRAZIONE_BUONO DESC",
            [
                maxLocalID[0]
            ]
        )

        rows = rows_to_dict_list(cursor)

        # i nuovi items vengono salvati in locale
        for row in rows:
            item_id = row['ID_INVENTARIO_BENI']
            description = row['DS_BENE']
            purchase_date = row['DT_REGISTRAZIONE_BUONO']
            price = row['VALORE_CONVENZIONALE']
            location = row['DS_SPAZIO']
            depreciation_starting_date = row['DT_INI_AMMORTAMENTO']

            item = Item(None,item_id,description,purchase_date,price,location,depreciation_starting_date)
            item.save()
        return redirect('showLocalDB')

    # Se non ci sono nuovi items viene ritornato un messaggio
    else:
        # localRows = Item.objects.using('default').all().order_by('-item_id')
        # context = {
        #     'rows': localRows,
        #     'message': "Il Database e' aggiornato"
        # }
        # return render (request,'prova/provaLocal.html',context)
        return redirect('showLocalDB')


def showSingleItem(request, local_id):
    print local_id
    item = Item.objects.get(id=local_id)
    context ={
        'id': item.id,
        'item_id': item.item_id,
        'description': item.description,
        'purchase_date': item.purchase_date,
        'price': item.price,
        'location': item.location,
        'depreciation_starting_date': item.depreciation_starting_date,
    }
    return render (request, 'prova/singleItem.html', context)


def getData(request):
    
    # get string parameters from the url
    requestOrder = request.GET.get('order', None)
    sort = request.GET.get('sort', None)
    search = request.GET.get('search', None)
    # get numeric parameter if they are defined in the url to avoid None conversion exceptions
    # if limit is not defined in the url it is set as the number of objects in the database
    limit = int(request.GET.get('limit')) if (request.GET.get('limit') is not None) else Item.objects.count()
    offset = int(request.GET.get('offset')) if (request.GET.get('offset') is not None) else 0

    # the number of object retrieved, default value is 0, will be calculated afterwards
    total = 0

    # if sort is defined the order must be according to the field specified
    if sort is not None:
        # if the order is asc we must prepend a "-" to the sort (ex. order by item_id asc -> order by -item_id)
        order = sort if requestOrder == 'asc' else '-' + sort
    else:
        # default is order by item_id asc
        order = '-item_id'

    # if search is defined we filter the results with the case-insensitive LIKE statement
    # of all the fields of the model
    if search is not None:

        # counts the number of objects that match the query
        total = Item.objects.using('default').filter(\
            Q(id__icontains= search) | \
            Q(item_id__icontains= search) | \
            Q(description__icontains = search) | \
            Q(purchase_date__icontains = search) | \
            Q(price__icontains = search) | \
            Q(location__icontains = search) | \
            Q(depreciation_starting_date__icontains = search) \
            ).count()

        # retrieve the objects that match the query
        rows = Item.objects.using('default').filter(\
            Q(id__icontains= search) | \
            Q(item_id__icontains= search) | \
            Q(description__icontains = search) | \
            Q(purchase_date__icontains = search) | \
            Q(price__icontains = search) | \
            Q(location__icontains = search) | \
            Q(depreciation_starting_date__icontains = search) \
            ).order_by(order)[offset:offset + limit]

    else:

        # counts the number of objects
        total = Item.objects.using('default').all().count()

        # retrieve the objects
        rows = Item.objects.using('default').all().order_by(order)[offset:offset + limit]
    
    # we construct the JSON response, we use json.dumps() to excape undesired characters
    html = '{ "total": ' + json.dumps(str(total)) + ', "rows": [ '
    for row in rows:
        html = html + '{ \
        "id": ' + json.dumps(str(row.id)) + ', \
        "item_id": ' + json.dumps(str(row.item_id)) + ', \
        "description": ' + json.dumps(row.description) + ', \
        "purchase_date": ' + json.dumps(str(row.purchase_date.date())) + ', \
        "price": ' + json.dumps(str(row.price)) + ', \
        "location": ' + json.dumps(row.location) + ', \
        "depreciation_starting_date": ' + json.dumps(str(row.depreciation_starting_date.date())) +  \
        ' }, '

    # remove last "," character for the last item
    if rows.count() > 0:
        html = html[0:len(html)-2]
    html = html + ' ] }'
    return HttpResponse(html)
