# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0012_bene_dt_registrazione_dg'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='descrizione_bene',
            field=models.CharField(default=b'', max_length=256),
        ),
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='possessore',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='ds_bene',
            field=models.CharField(max_length=400, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='pg_bene_sub',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='ubicazione_precisa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='inventario.UbicazionePrecisa', null=True),
        ),
    ]
