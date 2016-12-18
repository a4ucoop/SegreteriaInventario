# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0025_remove_ricognizioneinventariale_inventario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventario',
            name='id',
        ),
        migrations.AlterField(
            model_name='inventario',
            name='cd_invent',
            field=models.CharField(max_length=8, serialize=False, primary_key=True),
        ),
    ]
