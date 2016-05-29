# -*- coding: utf-8 -*-

from django import forms
from models import Bene
from inventario.models import RicognizioneInventariale

from django.forms.widgets import Select


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
		label='numero inventario minimo', 
		min_value=0
	)
	max_pg_bene = forms.IntegerField(		
		required=False,
		label='numero inventario massimo', 
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
	min_amm_iva_detr = forms.IntegerField(		
		required=False,
		label='valore ammortato minimo', 
		min_value=0
	)
	max_amm_iva_detr = forms.IntegerField(		
		required=False,
		label='valore ammortato massimo', 
		min_value=0
	)
	min_amm_iva_indetr = forms.IntegerField(		
		required=False,
		label='valore residuo minimo', 
		min_value=0
	)
	max_amm_iva_indetr = forms.IntegerField(		
		required=False,
		label='valore residuo massimo', 
		min_value=0
	)
	nome_tipo_dg = forms.CharField(		
		required=False,
		label='tipo documento', 
		max_length=None
	)
	min_num_doc_rif = forms.IntegerField(		
		required=False,
		label='numero documento minimo', 
		min_value=0
	)
	max_num_doc_rif = forms.IntegerField(		
		required=False,
		label='numero documento massmo', 
		min_value=0
	)
	min_num_registrazione = forms.IntegerField(		
		required=False,
		label='numero registrazione minimo', 
		min_value=0
	)
	max_num_registrazione = forms.IntegerField(		
		required=False,
		label='numero registrazione massmo', 
		min_value=0
	)
	denominazione = forms.CharField(		
		required=False,
		label='fornitore', 
		max_length=None
	)

class RicognizioneInventarialeForm(forms.ModelForm):
    class Meta:
        model = RicognizioneInventariale
        fields = ['cd_invent','pg_bene','pg_bene_sub','ds_spazio','ubicazione_precisa','ds_bene','immagine']
        widgets = {
            'ds_spazio' : Select(choices=[('','---------')] + [(item,item) for item in Bene.objects.using('default').values_list('ds_spazio', flat=True).distinct()]),
        }


class AdvancedSearchRicognizioneInventarialeForm(forms.Form):
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
		label='numero inventario minimo', 
		min_value=0
	)
	max_pg_bene = forms.IntegerField(		
		required=False,
		label='numero inventario massimo', 
		min_value=0
	)
	ds_bene = forms.CharField(		
		required=False,
		label='descrizione', 
		max_length=None
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
