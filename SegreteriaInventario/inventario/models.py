from django.db import models

class UbicazionePrecisa(models.Model):
	ubicazione = models.CharField(max_length=2000)

	def __str__(self):		# __unicode__ on Python 2
		return self.ubicazione

class Bene(models.Model):
	id_bene = models.IntegerField(default=None)
	cd_invent = models.CharField(max_length=8)
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
	valore_residuo = models.DecimalField(max_digits=15, decimal_places=2)
	immagine = models.FileField(upload_to='pictures/%Y/%m/%d', null=True)

class RicognizioneInventariale(models.Model):
	cd_invent = models.CharField(max_length=8)
	pg_bene = models.IntegerField(default=None)
	pg_bene_sub = models.IntegerField(default=None)
	ds_bene = models.CharField(max_length=400, null=True)
	ds_spazio = models.CharField(max_length=2000, null=True)
	ubicazione_precisa = models.ForeignKey(UbicazionePrecisa, null=True, on_delete=models.SET_NULL)
	immagine = models.FileField(upload_to='pictures/%Y/%m/%d', blank=True, null=True)
