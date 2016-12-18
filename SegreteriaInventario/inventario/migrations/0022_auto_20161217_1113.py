# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0021_auto_20161216_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='descrizione_bene',
            field=models.CharField(default=b'', max_length=256),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='ds_spazio',
            field=models.CharField(default=None, max_length=2000),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='pg_bene',
            field=models.IntegerField(default=-1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='pg_bene_sub',
            field=models.IntegerField(default=-1, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='possessore',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
