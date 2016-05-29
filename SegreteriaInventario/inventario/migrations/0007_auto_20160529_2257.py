# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_ricognizioneinventariale_ds_bene'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bene',
            name='valore_residuo',
        ),
        migrations.AddField(
            model_name='bene',
            name='amm_iva_detr',
            field=models.DecimalField(default=None, max_digits=15, decimal_places=2),
        ),
        migrations.AddField(
            model_name='bene',
            name='amm_iva_indetr',
            field=models.DecimalField(default=None, max_digits=15, decimal_places=2),
        ),
        migrations.AddField(
            model_name='bene',
            name='denominazione',
            field=models.CharField(default=None, max_length=256),
        ),
        migrations.AddField(
            model_name='bene',
            name='nome_tipo_dg',
            field=models.CharField(default=None, max_length=128),
        ),
        migrations.AddField(
            model_name='bene',
            name='num_doc_rif',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='bene',
            name='num_registrazione',
            field=models.IntegerField(default=None),
        ),
    ]
