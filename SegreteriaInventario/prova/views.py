from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.db import connections
from django.shortcuts import redirect
from models import Item
import datetime

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
            rownum < 10"
    	)
    
    rows = rows_to_dict_list(cursor)

    context = {'rows': rows}

    return render (request,'prova/provaRemote.html',context)



def showLocalDB(request):
    rows = Item.objects.using('default').all().order_by('-item_id')
    context ={'rows': rows}
    return render (request,'prova/provaLocal.html',context)



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