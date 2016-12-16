# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0017_auto_20161215_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='note',
            field=models.CharField(max_length=400, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='ds_bene',
            field=models.CharField(default=b'', max_length=400),
        ),
    ]
