# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0009_auto_20160531_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='bene',
            name='cognome',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='bene',
            name='nome',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
