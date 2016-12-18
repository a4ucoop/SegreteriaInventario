# -*- coding: utf-8 -*-

from django import forms
from models import Bene, Esse3User
from inventario.models import RicognizioneInventariale
from dal import autocomplete

from django.forms.widgets import Select

from django.contrib.auth.models import User
from models import Inventario


class PictureForm(forms.Form):
	# foto da caricare
    picture = forms.FileField(
        label='Select a file'
    )
    # id dell'item a cui appartiene la foto
    id_bene = forms.IntegerField(widget=forms.HiddenInput())

# ricavo tutti i codici degli inventari
codici_inventario = Bene.objects.using('default').values_list('cd_invent', 'ds_invent').distinct()
codici_inventario = filter(None, codici_inventario)
lista_codici = []
# metto i codici in una lista
for c in codici_inventario:
	lista_codici.append(
		(c[0],c[0])
	)
# li converto in tupla per passarli alla form
codici_inventario = lista_codici

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
	min_id_bene = forms.IntegerField(		
		required=False,
		label='id minimo', 
		min_value=0,
	)
	max_id_bene = forms.IntegerField(		
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
		label='edificio', 
		max_length=None
	)
	ubicazione_precisa = forms.CharField(		
		required=False,
		label='locale', 
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
	nome_tipo_dg = forms.CharField(		
		required=False,
		label='tipo documento', 
		max_length=None
	)
	num_doc_rif = forms.CharField(		
		required=False,
		label='numero documento', 
		max_length=None
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
	dt_registrazione_dg = forms.IntegerField(		
		required=False,
		label='Anno di registrazione del documento', 
		min_value=0
	)
	denominazione = forms.CharField(		
		required=False,
		label='fornitore', 
		max_length=None
	)
	nome = forms.CharField(		
		required=False,
		label='nome possessore', 
		max_length=None
	)
	cognome = forms.CharField(		
		required=False,
		label='cognome possessore', 
		max_length=None
	)

class RicognizioneInventarialeForm(forms.ModelForm):

    #possessore = forms.ChoiceField(label='Possessore',widget=Select(choices=[('','---------')] + [(item[0], item[1] + " " + item[2] ) for item in User.objects.using('default').values_list('username', 'first_name', 'last_name').distinct()]))
    #possessore = forms.ModelChoiceField(
    #    label='Possessore',
    #    queryset=Esse3User.objects.using('default').all(),
    #    widget=autocomplete.ModelSelect2(url='esse3user-autocomplete'))

#    def __init__(self, *args, **kwargs):
#        super(RicognizioneInventarialeForm, self).__init__(*args, **kwargs)
#        for name, field in self.fields.items():
#        	if field == 'descrizione_bene':
#        		field.widget = forms.TextInput(attrs={ 'required': 'true' })
            # if field.widget.__class__ == forms.widgets.TextInput:
            #     if field.widget.attrs.has_key('class'):
            #         field.widget.attrs['class'] += ' my-class'
            #     else:
            #         field.widget.attrs.update({'class':'my-class'})

    class Meta:
        model = RicognizioneInventariale
        fields = [
        	'id',
        	'ds_bene',
        	'inventario',
        	'pg_bene',
        	'pg_bene_sub',
        	'ds_spazio',
        	'ubicazione_precisa',
        	'note',
        	'immagine',
        	'possessore', 
        	'nuovo_possessore', 
        	'inserito_da']
        labels = {
            'ds_bene' : 'Descrizione',
            'possessore' : 'Possessore',
            'nuovo_possessore' : 'Nuovo Possessore',
            'inserito_da' : 'Inserito Da',
            'inventario' : 'Inventario',
            'pg_bene': 'Numero Inventario',
            'pg_bene_sub': 'Numero Bene Collegato',
            'ds_spazio': 'Edificio',
            'note': 'Note',
            'ubicazione_precisa': 'Locale',
        }
        widgets = {
            'pg_bene' : forms.TextInput(),
        	'pg_bene_sub' : forms.TextInput(),
            'ds_spazio' : Select(choices=[('','---------')] + [(item,item) for item in Bene.objects.using('default').values_list('ds_spazio', flat=True).distinct()]),
        }


# ricavo tutti i codici degli inventari
codici_inventario_ricinv = Inventario.objects.using('default').values_list('cd_invent', 'ds_invent').distinct()
codici_inventario_ricinv = filter(None, codici_inventario_ricinv)
lista_codici_ricinv = []
# metto i codici in una lista
for c in codici_inventario_ricinv:
	lista_codici_ricinv.append(
		(c[0],c[0])
	)
# li converto in tupla per passarli alla form
codici_inventario_ricinv = lista_codici_ricinv

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
        choices=codici_inventario_ricinv
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
	possessore = forms.CharField(		
		required=False,
		label='possessore', 
		max_length=None
	)
	ubicazione = forms.CharField(		
		required=False,
		label='edificio', 
		max_length=None
	)
	ubicazione_precisa = forms.CharField(		
		required=False,
		label='locale', 
		max_length=None
	)
