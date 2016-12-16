# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0019_ricognizioneinventariale_nuovo_possessore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='cd_invent',
            field=models.CharField(max_length=8, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='descrizione_bene',
            field=models.CharField(default=b'', max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='ds_bene',
            field=models.CharField(default=b'', max_length=400, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='ds_invent',
            field=models.CharField(default=None, max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='ds_spazio',
            field=models.CharField(max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='nuovo_possessore',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='pg_bene',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='pg_bene_sub',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='possessore',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
