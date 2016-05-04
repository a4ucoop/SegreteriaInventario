# -*- coding: utf-8 -*-

from django import forms
from models import Bene


class PictureForm(forms.Form):
	# foto da caricare
    picture = forms.FileField(
        label='Select a file'
    )
    # id dell'item a cui appartiene la foto
    id = forms.IntegerField(widget=forms.HiddenInput())

# ricavo tutti i codici degli inventari
codici_inventario = Bene.objects.using('default').values_list('cd_invent', flat=True).distinct()
codici_inventario = filter(None, codici_inventario)
lista_codici = []
# metto i codici in una lista
for c in codici_inventario:
	lista_codici.append(
		(c, c)
	)
# li converto in tupla per passarli alla form
codici_inventario = tuple(lista_codici)

# ricavo tutte le categorie inventariali
categorie_inventariali = Bene.objects.using('default').values_list('ds_categ_gruppo', flat=True).distinct()
categorie_inventariali = filter(None, categorie_inventariali)
lista_categorie = []
# metto le categorie in una lista
for ci in categorie_inventariali:
	lista_categorie.append(
		(ci, ci)
	)
# converto le categorie per passarle alla form
categorie_inventariali = tuple(lista_categorie)

class AdvancedSearchForm(forms.Form):
	min_id = forms.IntegerField(		
		required=False,
		label='id minimo', 
		min_value=0,
	)
	max_id = forms.IntegerField(		
		required=False,
		label='id massimo', 
		min_value=0,
	)
	codice_inventario = forms.MultipleChoiceField(
		required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=codici_inventario
    )
	min_pg_bene = forms.IntegerField(		
		required=False,
		label='pg minimo', 
		min_value=0
	)
	max_pg_bene = forms.IntegerField(		
		required=False,
		label='pg massimo', 
		min_value=0
	)
	ds_bene = forms.CharField(		
		required=False,
		label='descrizione', 
		max_length=None
	)
	from_dt_acquisto = forms.DateField(		
		required=False,
		label='data acquisto inizio',
	)
	to_dt_acquisto = forms.DateField(		
		required=False,
		label='data acquisto fine',
	)
	categorie_inventariali = forms.MultipleChoiceField(
		required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=categorie_inventariali
    )
	ubicazione = forms.CharField(		
		required=False,
		label='ubicazione', 
		max_length=None
	)
	ubicazione_precisa = forms.CharField(		
		required=False,
		label='ubicazione precisa', 
		max_length=None
	)
	from_dt_ini_ammortamento = forms.DateField(		
		required=False,
		label='data inizio ammortamento inizio',
	)
	to_dt_ini_ammortamento = forms.DateField(		
		required=False,
		label='data inizio ammortamento fine',
	)
	min_valore_convenzionale = forms.IntegerField(		
		required=False,
		label='prezzo minimo', 
		min_value=0
	)
	max_valore_convenzionale = forms.IntegerField(		
		required=False,
		label='prezzo massimo', 
		min_value=0
	)	
	min_valore_residuo = forms.IntegerField(		
		required=False,
		label='valore residuo minimo', 
		min_value=0
	)
	max_valore_residuo = forms.IntegerField(		
		required=False,
		label='valore residuo massimo', 
		min_value=0
	)