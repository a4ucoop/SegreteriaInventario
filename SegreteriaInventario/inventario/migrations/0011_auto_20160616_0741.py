# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0010_auto_20160606_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='bene',
            name='ds_invent',
            field=models.CharField(default=None, max_length=256),
        ),
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='ds_invent',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
    ]
