# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0022_auto_20161217_1113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ricognizioneinventariale',
            name='descrizione_bene',
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='ds_bene',
            field=models.CharField(default=b'', max_length=400),
        ),
    ]
