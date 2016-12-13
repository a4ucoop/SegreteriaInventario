from django.db import models

from django.contrib.auth.models import User

class UbicazionePrecisa(models.Model):
	ubicazione = models.CharField(max_length=2000)

	def __str__(self):		# __unicode__ on Python 2
		return self.ubicazione

class Bene(models.Model):
    id_bene = models.IntegerField(default=None)
    cd_invent = models.CharField(max_length=8)
    ds_invent = models.CharField(max_length=256,default=None)
    pg_bene = models.IntegerField(default=None)
    pg_bene_sub = models.IntegerField(default=None)
    ds_bene = models.CharField(max_length=400)
    dt_registrazione_buono = models.DateTimeField('data registrazione buono')
    cd_categ_gruppo = models.CharField(max_length=60)
    ds_categ_gruppo = models.CharField(max_length=255)
    ds_spazio = models.CharField(max_length=2000)
    ubicazione_precisa = models.ForeignKey(UbicazionePrecisa, null=True, on_delete=models.SET_NULL)
    dt_ini_ammortamento = models.DateTimeField('data inizio ammortamento')
    valore_convenzionale = models.DecimalField(max_digits=15, decimal_places=2)
    nome_tipo_dg = models.CharField(max_length=128,default=None)
    num_doc_rif = models.CharField(max_length=128,default=None)
    num_registrazione = models.IntegerField(default=None)
    dt_registrazione_dg =models.IntegerField('anno di registrazione documento',default=None)
    denominazione = models.CharField(max_length=256,default=None)
    nome = models.CharField(max_length=128,default=None, null = True)
    cognome = models.CharField(max_length=128,default=None, null = True)
    immagine = models.FileField(upload_to='pictures/%Y/%m/%d', null=True)

class RicognizioneInventariale(models.Model):
    descrizione_bene = models.CharField(max_length=256, default='')
    possessore = models.ForeignKey('Esse3User',default=None,related_name='ricinv_possessori')
    inserito_da = models.ForeignKey(User, default=None, related_name='ricinv_inseritori')
    cd_invent = models.CharField(max_length=8)
    ds_invent = models.CharField(max_length=256,default=None,null=True)
    pg_bene = models.IntegerField(default=None)
    pg_bene_sub = models.IntegerField(default=0)
    ds_bene = models.CharField(max_length=400, blank=True, null=True)
    ds_spazio = models.CharField(max_length=2000, null=True)
    ubicazione_precisa = models.ForeignKey(UbicazionePrecisa,blank=True, null=True, on_delete=models.SET_NULL)
    immagine = models.FileField(upload_to='pictures/%Y/%m/%d', blank=True, null=True)

class Esse3User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
