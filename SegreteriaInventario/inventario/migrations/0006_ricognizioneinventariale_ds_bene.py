# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_ricognizioneinventariale'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='ds_bene',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
