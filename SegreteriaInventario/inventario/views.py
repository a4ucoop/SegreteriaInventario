from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.db import connections
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import login as django_auth_login
from models import Bene
from models import UbicazionePrecisa
from forms import PictureForm
from forms import AdvancedSearchForm
import datetime
import json

def index(request):
	return showLocalDB(request)

@never_cache
def login(request, *args, **kw):
    print request, args, kw
    return django_auth_login(request, *args, **kw)

def registration(request):
    """TODO"""
    return ""

# prende il cursore che ha eseguito la query, estrae i risultati sotto
# forma di dizionario che ha come chiave il nome del campo
def rows_to_dict_list(cursor):
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in cursor]


@login_required
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
		    	INV.DT_INI_AMMORTAMENTO,\
                INV.VALORE_CONVENZIONALE - \
                (LEAST((extract(year from sysdate) - EXTRACT(year FROM INV.DT_INI_AMMORTAMENTO)),AMM.NUM_ANNUALITA) * \
                    (INV.VALORE_CONVENZIONALE / AMM.NUM_ANNUALITA)) AS VALORE_RESIDUO\
	    	FROM\
	    		(((V_IE_CO_MOVIMENTI_BENE MOV INNER JOIN V_IE_CO_INVENTARIO_BENI INV\
	    		ON MOV.ID_INVENTARIO_BENI = INV.ID_INVENTARIO_BENI) INNER JOIN\
	    		V_IE_AC_SPAZI SPA ON INV.CD_UBICAZIONE = SPA.CD_SPAZIO) INNER JOIN\
                V_IE_CO_AS_TIP_AMM_CAT_GRP_INV AMM on INV.CD_CATEG_GRUPPO = AMM.CD_CATEG_GRUPPO )\
	    	ORDER BY\
	    		MOV.ID_INVENTARIO_BENI DESC\
    		)\
        WHERE\
            rownum < 100"
    	)

    rows = rows_to_dict_list(cursor)

    context = {'rows': rows}

    return render (request,'inventario/inventarioRemoto.html',context)



@login_required
def showLocalDB(request):
    picform = PictureForm()  # costruisce una form per l'upload dell'immagine
    asform = AdvancedSearchForm()  # costruisce una form per l'upload dell'immagine
    # prende le location dal DB per popolare il menu della quicksearch
    locations = Bene.objects.using('default').values_list('ds_spazio', flat=True).distinct()
    locations = filter(None, locations)
    locations = [l.split('-')[0].lower() for l in locations]
    # prende le accurateLocation dal DB per popolare il menu della quicksearch
    accurateLocations = UbicazionePrecisa.objects.using('default').all()
    context ={'locations': locations, 'accurateLocations': accurateLocations, 'picform': picform, 'asform': asform}
    return render (request,'inventario/inventarioLocale.html',context)



@login_required
def updateLocalDB(request):
    cursor = connections['cineca'].cursor()         # Cursor connessione Cineca
    cursorLocal = connections['default'].cursor()   # Cursor DB locale

    # Seleziona tutti i dati necessari dal DB remoto
    cursor.execute(
        "SELECT DISTINCT\
                INV.ID_INVENTARIO_BENI,\
                INV.CD_INVENT,\
                INV.PG_BENE,\
                INV.PG_BENE_SUB,\
                INV.DS_BENE,\
                MOV.DT_REGISTRAZIONE_BUONO,\
                INV.CD_CATEG_GRUPPO,\
                GRP.DS_CATEG_GRUPPO,\
                SPA.DS_SPAZIO,\
                INV.DT_INI_AMMORTAMENTO,\
                INV.VALORE_CONVENZIONALE,\
                INV.VALORE_CONVENZIONALE - (LEAST((extract(year from sysdate) - EXTRACT(year FROM INV.DT_INI_AMMORTAMENTO)), AMM.NUM_ANNUALITA) * (INV.VALORE_CONVENZIONALE / AMM.NUM_ANNUALITA)) AS VALORE_RESIDUO\
        FROM\
                ((((SIACO_UNICAM_PROD.V_IE_CO_INVENTARIO_BENI INV JOIN SIACO_UNICAM_PROD.V_IE_CO_CATEG_GRP_INVENT GRP\
                ON INV.CD_CATEG_GRUPPO = GRP.CD_CATEG_GRUPPO) JOIN SIACO_UNICAM_PROD.V_IE_AC_SPAZI SPA\
                ON INV.CD_UBICAZIONE = SPA.CD_SPAZIO) JOIN SIACO_UNICAM_PROD.V_IE_CO_MOVIMENTI_BENE MOV\
                ON INV.CD_INVENT = MOV.CD_INVENT AND INV.PG_BENE = MOV.PG_BENE AND INV.PG_BENE_SUB = MOV.PG_BENE_SUB) JOIN V_IE_CO_AS_TIP_AMM_CAT_GRP_INV AMM\
                ON INV.CD_CATEG_GRUPPO = AMM.CD_CATEG_GRUPPO)\
        WHERE\
            (AMM.ESERCIZIO - EXTRACT(year FROM INV.DT_INI_AMMORTAMENTO)) = 0"
        )

    rows = rows_to_dict_list(cursor)

    # Scorre tutti i dati riga per riga
    for row in rows:
        # Per ogni riga vede se l'oggetto esiste gia' nel database
        try:
            #print "obj ",row['ID_INVENTARIO_BENI'],"val res: ",row['VALORE_RESIDUO']
            bene = Bene.objects.get(cd_invent=row['CD_INVENT'], pg_bene=row['PG_BENE'], pg_bene_sub=row['PG_BENE_SUB'])

            # Se l'oggetto esiste i dati vengono aggiornati
            
            bene.id_bene = row['ID_INVENTARIO_BENI'] if row['ID_INVENTARIO_BENI'] is not None else -1
            bene.cd_invent = row['CD_INVENT'] if row['CD_INVENT'] is not None else -1
            bene.pg_bene = row['PG_BENE'] if row['PG_BENE'] is not None else -1
            bene.pg_bene_sub = row['PG_BENE_SUB'] if row['PG_BENE_SUB'] is not None else -1
            bene.ds_bene = row['DS_BENE'] if row['DS_BENE'] is not None else ''
            bene.dt_registrazione_buono = row['DT_REGISTRAZIONE_BUONO'] if row['DT_REGISTRAZIONE_BUONO'] is not None else '0001-01-01 00:00'
            bene.cd_categ_gruppo = row['CD_CATEG_GRUPPO'] if row['CD_CATEG_GRUPPO'] is not None else ''
            bene.ds_categ_gruppo = row['DS_CATEG_GRUPPO'] if row['DS_CATEG_GRUPPO'] is not None else ''
            bene.ds_spazio = row['DS_SPAZIO'] if row['DS_SPAZIO'] is not None else ''
            bene.dt_ini_ammortamento = row['DT_INI_AMMORTAMENTO'] if row['DT_INI_AMMORTAMENTO'] is not None else '0001-01-01 00:00'
            bene.valore_convenzionale = row['VALORE_CONVENZIONALE'] if row['VALORE_CONVENZIONALE'] is not None else ''
            bene.valore_residuo = row['VALORE_RESIDUO'] if row['VALORE_RESIDUO'] is not None else -1

            # item = Item(None,item_id,description,purchase_date,price,location,depreciation_starting_date)
            bene.save()
        except Bene.DoesNotExist:
            # Se non esiste viene creato un nuovo oggetto
            bene.id_bene = row['ID_INVENTARIO_BENI'] if row['ID_INVENTARIO_BENI'] is not None else -1
            cd_invent = row['CD_INVENT'] if row['CD_INVENT'] is not None else -1
            pg_bene = row['PG_BENE'] if row['PG_BENE'] is not None else -1
            pg_bene_sub = row['PG_BENE_SUB'] if row['PG_BENE_SUB'] is not None else -1
            ds_bene = row['DS_BENE'] if row['DS_BENE'] is not None else ''
            dt_registrazione_buono = row['DT_REGISTRAZIONE_BUONO'] if row['DT_REGISTRAZIONE_BUONO'] is not None else '0001-01-01 00:00'
            cd_categ_gruppo = row['CD_CATEG_GRUPPO'] if row['CD_CATEG_GRUPPO'] is not None else ''
            ds_categ_gruppo = row['DS_CATEG_GRUPPO'] if row['DS_CATEG_GRUPPO'] is not None else ''
            ds_spazio = row['DS_SPAZIO'] if row['DS_SPAZIO'] is not None else ''
            dt_ini_ammortamento = row['DT_INI_AMMORTAMENTO'] if row['DT_INI_AMMORTAMENTO'] is not None else '0001-01-01 00:00'
            valore_convenzionale = row['VALORE_CONVENZIONALE'] if row['VALORE_CONVENZIONALE'] is not None else ''
            valore_residuo = row['VALORE_RESIDUO'] if row['VALORE_RESIDUO'] is not None else -1
            bene = Bene(id_bene = id_bene, 
                        cd_invent = cd_invent, 
                        pg_bene = pg_bene,
                        pg_bene_sub = pg_bene_sub,
                        ds_bene = ds_bene,
                        dt_registrazione_buono = dt_registrazione_buono,
                        cd_categ_gruppo = cd_categ_gruppo,
                        ds_categ_gruppo = ds_categ_gruppo,
                        ds_spazio = ds_spazio,
                        dt_ini_ammortamento = dt_ini_ammortamento,
                        valore_convenzionale = valore_convenzionale,
                        valore_residuo = valore_residuo) 
            bene.save()

    return redirect ('showLocalDB')



@login_required
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
        "SELECT max(id_bene)\
         FROM inventario_bene;"
    )

    maxRemoteID = cursor.fetchone()
    maxLocalID = cursorLocal.fetchone()

    # Se gli id sono diversi sono stati inseriti nuovi dati
    if maxRemoteID > maxLocalID:
        # Vengono ricavati tutti i nuovi items ovvero
        # quelli che hanno ID maggiore del massimo locale
        cursor.execute(
            "SELECT DISTINCT\
                    INV.ID_INVENTARIO_BENI,\
                    INV.CD_INVENT,\
                    INV.PG_BENE,\
                    INV.PG_BENE_SUB,\
                    INV.DS_BENE,\
                    MOV.DT_REGISTRAZIONE_BUONO,\
                    INV.CD_CATEG_GRUPPO,\
                    GRP.DS_CATEG_GRUPPO,\
                    SPA.DS_SPAZIO,\
                    INV.DT_INI_AMMORTAMENTO,\
                    INV.VALORE_CONVENZIONALE,\
                    INV.VALORE_CONVENZIONALE - (LEAST((extract(year from sysdate) - EXTRACT(year FROM INV.DT_INI_AMMORTAMENTO)), AMM.NUM_ANNUALITA) * (INV.VALORE_CONVENZIONALE / AMM.NUM_ANNUALITA)) AS VALORE_RESIDUO\
            FROM\
                    ((((SIACO_UNICAM_PROD.V_IE_CO_INVENTARIO_BENI INV JOIN SIACO_UNICAM_PROD.V_IE_CO_CATEG_GRP_INVENT GRP\
                    ON INV.CD_CATEG_GRUPPO = GRP.CD_CATEG_GRUPPO) JOIN SIACO_UNICAM_PROD.V_IE_AC_SPAZI SPA\
                    ON INV.CD_UBICAZIONE = SPA.CD_SPAZIO) JOIN SIACO_UNICAM_PROD.V_IE_CO_MOVIMENTI_BENE MOV\
                    ON INV.CD_INVENT = MOV.CD_INVENT AND INV.PG_BENE = MOV.PG_BENE AND INV.PG_BENE_SUB = MOV.PG_BENE_SUB) JOIN V_IE_CO_AS_TIP_AMM_CAT_GRP_INV AMM\
                    ON INV.CD_CATEG_GRUPPO = AMM.CD_CATEG_GRUPPO)\
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
            # Se non esiste viene creato un nuovo oggetto
            id_bene = row['ID_INVENTARIO_BENI'] if row['ID_INVENTARIO_BENI'] is not None else -1
            cd_invent = row['CD_INVENT'] if row['CD_INVENT'] is not None else -1
            pg_bene = row['PG_BENE'] if row['PG_BENE'] is not None else -1
            pg_bene_sub = row['PG_BENE_SUB'] if row['PG_BENE_SUB'] is not None else -1
            ds_bene = row['DS_BENE'] if row['DS_BENE'] is not None else ''
            dt_registrazione_buono = row['DT_REGISTRAZIONE_BUONO'] if row['DT_REGISTRAZIONE_BUONO'] is not None else '0001-01-01 00:00'
            cd_categ_gruppo = row['CD_CATEG_GRUPPO'] if row['CD_CATEG_GRUPPO'] is not None else ''
            ds_categ_gruppo = row['DS_CATEG_GRUPPO'] if row['DS_CATEG_GRUPPO'] is not None else ''
            ds_spazio = row['DS_SPAZIO'] if row['DS_SPAZIO'] is not None else ''
            dt_ini_ammortamento = row['DT_INI_AMMORTAMENTO'] if row['DT_INI_AMMORTAMENTO'] is not None else '0001-01-01 00:00'
            valore_convenzionale = row['VALORE_CONVENZIONALE'] if row['VALORE_CONVENZIONALE'] is not None else ''
            valore_residuo = row['VALORE_RESIDUO'] if row['VALORE_RESIDUO'] is not None else -1
            bene = Bene(id_bene = id_bene, 
                        cd_invent = cd_invent, 
                        pg_bene = pg_bene,
                        pg_bene_sub = pg_bene_sub,
                        ds_bene = ds_bene,
                        dt_registrazione_buono = dt_registrazione_buono,
                        cd_categ_gruppo = cd_categ_gruppo,
                        ds_categ_gruppo = ds_categ_gruppo,
                        ds_spazio = ds_spazio,
                        dt_ini_ammortamento = dt_ini_ammortamento,
                        valore_convenzionale = valore_convenzionale,
                        valore_residuo = valore_residuo) 
            bene.save()
        return redirect('showLocalDB')

    # Se non ci sono nuovi items viene ritornato un messaggio
    else:
        # localRows = Item.objects.using('default').all().order_by('-item_id')
        # context = {
        #     'rows': localRows,
        #     'message': "Il Database e' aggiornato"
        # }
        # return render (request,'inventario/inventarioLocale.html',context)
        return redirect('showLocalDB')


@login_required
def showSingleItem(request, local_id):
    bene = Bene.objects.get(id=local_id)
    context ={
        'id': bene.id,
        'cd_invent': bene.cd_invent,
        'pg_bene': bene.pg_bene,
        'pg_bene_sub': bene.pg_bene_sub,
        'ds_bene': bene.ds_bene,
        'dt_registrazione_buono': bene.dt_registrazione_buono,
        'cd_categ_gruppo': bene.cd_categ_gruppo,
        'ds_categ_gruppo': bene.ds_categ_gruppo,
        'ds_spazio': bene.ds_spazio,
        'ubicazione_precisa': bene.ubicazione_precisa,
        'dt_ini_ammortamento': bene.dt_ini_ammortamento,
        'valore_convenzionale': bene.valore_convenzionale,
        'valore_residuo': bene.valore_residuo,
        'immagine': bene.immagine,
    }
    return render (request, 'inventario/beneSingolo.html', context)

@login_required
def getData(request):
    
    # get string parameters from the url
    requestOrder = request.GET.get('order', None)
    sort = request.GET.get('sort', None)
    search = request.GET.get('search', None)
    # get numeric parameter if they are defined in the url to avoid None conversion exceptions
    # if limit is not defined in the url it is set as the number of objects in the database
    limit = int(request.GET.get('limit')) if (request.GET.get('limit') is not None) else Bene.objects.count()
    offset = int(request.GET.get('offset')) if (request.GET.get('offset') is not None) else 0

    # the number of object retrieved, default value is 0, will be calculated afterwards
    total = 0

    # if sort is defined the order must be according to the field specified
    if sort is not None:
        # if the order is asc we must prepend a "-" to the sort (ex. order by bene_id asc -> order by -bene_id)
        order = sort if requestOrder == 'asc' else '-' + sort
    else:
        # default is order by bene_id asc
        order = '-id_bene'

    # if search is defined we filter the results with the case-insensitive LIKE statement
    # of all the fields of the model
    if search is not None:

        # counts the number of objects that match the query
        total = Bene.objects.using('default').filter(\
            Q(id__icontains= search) | \
            Q(cd_invent__icontains= search) | \
            Q(pg_bene__icontains= search) | \
            Q(pg_bene_sub__icontains= search) | \
            Q(ds_bene__icontains= search) | \
            Q(dt_registrazione_buono__icontains= search) | \
            Q(cd_categ_gruppo__icontains= search) | \
            Q(ds_categ_gruppo__icontains= search) | \
            Q(ds_spazio__icontains= search) | \
            Q(ubicazione_precisa__ubicazione__icontains= search) | \
            Q(dt_ini_ammortamento__icontains= search) | \
            Q(valore_convenzionale__icontains= search) | \
            Q(valore_residuo__icontains= search) \
            ).count()

        # retrieve the objects that match the query
        rows = Bene.objects.using('default').filter(\
            Q(id__icontains= search) | \
            Q(cd_invent__icontains= search) | \
            Q(pg_bene__icontains= search) | \
            Q(pg_bene_sub__icontains= search) | \
            Q(ds_bene__icontains= search) | \
            Q(dt_registrazione_buono__icontains= search) | \
            Q(cd_categ_gruppo__icontains= search) | \
            Q(ds_categ_gruppo__icontains= search) | \
            Q(ds_spazio__icontains= search) | \
            Q(ubicazione_precisa__ubicazione__icontains= search) | \
            Q(dt_ini_ammortamento__icontains= search) | \
            Q(valore_convenzionale__icontains= search) | \
            Q(valore_residuo__icontains= search) \
            ).order_by(order)[offset:offset + limit]

    else:

        # counts the number of objects
        total = Bene.objects.using('default').all().count()

        # retrieve the objects
        rows = Bene.objects.using('default').all().order_by(order)[offset:offset + limit]
    
    # we construct the JSON response, we use json.dumps() to excape undesired characters
    html = '{ "total": ' + json.dumps(str(total)) + ', "rows": [ '
    for row in rows:
        # we get the id of the ubicazione_precisa because we need to display it instead of the text value (that will be matched with the list in the view)
        ubicazione_precisa = row.ubicazione_precisa.id if (row.ubicazione_precisa is not None) else None
        html = html + '{ \
        "id": ' + json.dumps(str(row.id)) + ', \
        "cd_invent": ' + json.dumps(row.cd_invent) + ', \
        "pg_bene": ' + json.dumps(str(row.pg_bene)) + ', \
        "pg_bene_sub": ' + json.dumps(str(row.pg_bene_sub)) + ', \
        "ds_bene": ' + json.dumps(row.ds_bene) + ', \
        "dt_registrazione_buono": ' + json.dumps(str(row.dt_registrazione_buono.date()) if row.dt_registrazione_buono is not None else "") + ', \
        "cd_categ_gruppo": ' + json.dumps(row.cd_categ_gruppo) + ', \
        "ds_categ_gruppo": ' + json.dumps(row.ds_categ_gruppo) + ', \
        "ds_spazio": ' + json.dumps(row.ds_spazio) + ', \
        "ubicazione_precisa": ' + json.dumps(str(row.ubicazione_precisa_id)) + ', \
        "dt_ini_ammortamento": ' + json.dumps(str(row.dt_ini_ammortamento.date()) if row.dt_ini_ammortamento is not None else "") + ', \
        "valore_convenzionale": ' + json.dumps(str(row.valore_convenzionale)) + ', \
        "valore_residuo": ' + json.dumps(str(row.valore_residuo)) + ', \
        "immagine": ' + json.dumps(str(row.immagine)) + \
        ' }, '

    # remove last "," character for the last item
    if rows.count() > 0:
        html = html[0:len(html)-2]
    html = html + ' ] }'
    return HttpResponse(html)

@login_required
def uploadPicture(request):
    # Handle file upload
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            id = int(form.cleaned_data['id'])
            try:
                bene = Bene.objects.get(id=id)          # ricava l'item di cui fare l'upload della foto dall'ID
                print request.FILES['picture']
                bene.immagine = request.FILES['picture'] # valorizza l'immagine con il path dove e' contenuta
                bene.save()
            except Bene.DoesNotExist:
                print "Il bene non esiste"

    # Redirect to the document list after POST
    return redirect ('showLocalDB')

@login_required
def editAccurateLocation(request):
    postID = int(request.POST.get("pk"))
    value = str(request.POST.get("value"))

    try:
        # we retrieve the item which must be edited
        bene = Bene.objects.get(id=postID)
        # we get the corrisponding accurateLocation obj, according to the id we received
        up = UbicazionePrecisa.objects.get(id=value)
        bene.ubicazione_precisa = up # we edit the location
        bene.save()
    except (Bene.DoesNotExist, UbicazionePrecisa.DoesNotExist):
        return HttpResponseServerError("Non e' stato possibile modificare il valore")

    return HttpResponse("OK")

@login_required
def getAccurateLocationList(request):
    list = "["
    # we get all the accurateLocation in the DB
    rows = UbicazionePrecisa.objects.using('default').all()
    # we create the JSON response according to the x-edit plugin data format
    for row in rows:
        list = list + "{ \"value\": \"" + str(row.id) + "\", " + "\"text\": " + json.dumps(str(row.ubicazione)) + "},"
    list = list[:-1] + "]"
    # the HttpResponse contains the JSON data
    return HttpResponse(list)

@login_required
def addAccurateLocation(request):
    nuovaUbicazione = str(request.POST.get("nuovaUbicazione"))
    up = UbicazionePrecisa()
    up.ubicazione = nuovaUbicazione
    up.save()
    return HttpResponse("OK")


@login_required
def advancedSearch(request):
    if request.method == 'GET':
        min_id = int(request.GET.get('min_id')) if (request.GET.get('min_id') is not None) else None
        max_id = int(request.GET.get('max_id')) if (request.GET.get('max_id') is not None) else None
        cods = request.GET.getlist('cods')
        min_pg_bene = int(request.GET.get('min_pg_bene')) if (request.GET.get('min_pg_bene') is not None) else None
        max_pg_bene = int(request.GET.get('max_pg_bene')) if (request.GET.get('max_pg_bene') is not None) else None
        ds_bene = request.GET.get('ds_bene')
        # da controllare il formato della data!
        from_dt_acquisto = datetime.datetime.strptime(request.GET.get('from_dt_acquisto'), "%d/%m/%Y") if (request.GET.get('from_dt_acquisto') is not None) else None
        to_dt_acquisto = datetime.datetime.strptime(request.GET.get('to_dt_acquisto'), "%d/%m/%Y") if (request.GET.get('to_dt_acquisto') is not None) else None
        categ = request.GET.getlist('categ')
        ubicazione = request.GET.get('ubicazione')
        ubicazione_precisa = request.GET.get('ubicazione_precisa')
        # da controllare il formato della data!
        from_dt_ini_ammortamento = datetime.datetime.strptime(request.GET.get('from_dt_ini_ammortamento'), "%d/%m/%Y") if (request.GET.get('from_dt_ini_ammortamento') is not None) else None
        to_dt_ini_ammortamento = datetime.datetime.strptime(request.GET.get('to_dt_ini_ammortamento'), "%d/%m/%Y") if (request.GET.get('to_dt_ini_ammortamento') is not None) else None
        min_valore_convenzionale = int(request.GET.get('min_valore_convenzionale')) if (request.GET.get('min_valore_convenzionale') is not None) else None
        max_valore_convenzionale = int(request.GET.get('max_valore_convenzionale')) if (request.GET.get('max_valore_convenzionale') is not None) else None
        min_valore_residuo = int(request.GET.get('min_valore_residuo')) if (request.GET.get('min_valore_residuo') is not None) else None
        max_valore_residuo = int(request.GET.get('max_valore_residuo')) if (request.GET.get('max_valore_residuo') is not None) else None

        # # stampe debug
        # print("min_id", min_id);
        # print("max_id", max_id);
        # print("cods", cods);
        # print("min_pg_bene", min_pg_bene);
        # print("max_pg_bene", max_pg_bene);
        # print("ds_bene", ds_bene);
        # print("from_dt_acquisto", from_dt_acquisto);
        # print("to_dt_acquisto", to_dt_acquisto);
        # print("categ", categ)
        # print("ubicazione", ubicazione);
        # print("ubicazione_precisa", ubicazione_precisa);
        # print("from_dt_ini_ammortamento", from_dt_ini_ammortamento);
        # print("to_dt_ini_ammortamento", to_dt_ini_ammortamento);
        # print("min_valore_convenzionale", min_valore_convenzionale);
        # print("max_valore_convenzionale", max_valore_convenzionale);
        # print("min_valore_residuo", min_valore_residuo);
        # print("max_valore_residuo", max_valore_residuo);

        requestOrder = request.GET.get('order', None)
        sort = request.GET.get('sort', None)
        # get numeric parameter if they are defined in the url to avoid None conversion exceptions
        # if limit is not defined in the url it is set as the number of objects in the database
        limit = int(request.GET.get('limit')) if (request.GET.get('limit') is not None) else Bene.objects.count()
        offset = int(request.GET.get('offset')) if (request.GET.get('offset') is not None) else 0

        # the number of object retrieved, default value is 0, will be calculated afterwards
        total = 0

        # if sort is defined the order must be according to the field specified
        if sort is not None:
            # if the order is asc we must prepend a "-" to the sort (ex. order by bene_id asc -> order by -bene_id)
            order = sort if requestOrder == 'asc' else '-' + sort
        else:
            # default is order by bene_id asc
            order = '-id_bene'
        
        rows = Bene.objects.using('default').all()
        # filter id range
        if (min_id is not None and max_id is not None):
            rows = rows.filter(id__range=(min_id, max_id))
        # filter inventory code in selection list
        if (cods is not None and cods):
            rows = rows.filter(cd_invent__in=cods)
        if (min_pg_bene is not None and max_pg_bene is not None):
            rows = rows.filter(pg_bene__range=(min_pg_bene, max_pg_bene))
        if (ds_bene is not None):
            rows = rows.filter(ds_bene__icontains=ds_bene)
        if (from_dt_acquisto is not None and to_dt_acquisto is not None):
            rows = rows.filter(dt_registrazione_buono__range=(from_dt_acquisto, to_dt_acquisto))
        if (categ is not None and categ):
            rows = rows.filter(ds_categ_gruppo__in=categ)
        if (ubicazione is not None):
            rows = rows.filter(ds_spazio__icontains=ubicazione)
        if (ubicazione is not None):
            rows = rows.filter(ds_spazio__icontains=ubicazione)
        if (ubicazione_precisa is not None):
            rows = rows.filter(ubicazione_precisa__ubicazione__icontains=ubicazione_precisa)
        if (from_dt_ini_ammortamento is not None and to_dt_ini_ammortamento is not None):
            rows = rows.filter(dt_ini_ammortamento__range=(from_dt_ini_ammortamento, to_dt_ini_ammortamento))
        if (min_valore_convenzionale is not None and max_valore_convenzionale is not None):
            rows = rows.filter(valore_convenzionale__range=(min_valore_convenzionale, max_valore_convenzionale))
        if (min_valore_residuo is not None and max_valore_residuo is not None):
            rows = rows.filter(valore_convenzionale__range=(min_valore_residuo, max_valore_residuo))

        total = rows.count();
        rows = rows.order_by(order)[offset:offset + limit]



        # we construct the JSON response, we use json.dumps() to excape undesired characters
        html = '{ "total": ' + json.dumps(str(total)) + ', "rows": [ '
        for row in rows:
            # we get the id of the ubicazione_precisa because we need to display it instead of the text value (that will be matched with the list in the view)
            ubicazione_precisa = row.ubicazione_precisa.id if (row.ubicazione_precisa is not None) else None
            html = html + '{ \
            "id": ' + json.dumps(str(row.id)) + ', \
            "cd_invent": ' + json.dumps(row.cd_invent) + ', \
            "pg_bene": ' + json.dumps(str(row.pg_bene)) + ', \
            "pg_bene_sub": ' + json.dumps(str(row.pg_bene_sub)) + ', \
            "ds_bene": ' + json.dumps(row.ds_bene) + ', \
            "dt_registrazione_buono": ' + json.dumps(str(row.dt_registrazione_buono.date()) if row.dt_registrazione_buono is not None else "") + ', \
            "cd_categ_gruppo": ' + json.dumps(row.cd_categ_gruppo) + ', \
            "ds_categ_gruppo": ' + json.dumps(row.ds_categ_gruppo) + ', \
            "ds_spazio": ' + json.dumps(row.ds_spazio) + ', \
            "ubicazione_precisa": ' + json.dumps(str(row.ubicazione_precisa_id)) + ', \
            "dt_ini_ammortamento": ' + json.dumps(str(row.dt_ini_ammortamento.date()) if row.dt_ini_ammortamento is not None else "") + ', \
            "valore_convenzionale": ' + json.dumps(str(row.valore_convenzionale)) + ', \
            "valore_residuo": ' + json.dumps(str(row.valore_residuo)) + ', \
            "immagine": ' + json.dumps(str(row.immagine)) + \
            ' }, '

        # remove last "," character for the last item
        if rows.count() > 0:
            html = html[0:len(html)-2]
        html = html + ' ] }'
        return HttpResponse(html)
        # Redirect to the document list after POST
        return redirect ('showLocalDB')