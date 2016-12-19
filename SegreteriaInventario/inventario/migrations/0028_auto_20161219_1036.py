# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0027_ricognizioneinventariale_inventario'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='cognome',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='nome',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
