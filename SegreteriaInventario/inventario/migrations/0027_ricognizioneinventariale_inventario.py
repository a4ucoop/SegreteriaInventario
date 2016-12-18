# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0026_auto_20161217_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='inventario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='inventario.Inventario', null=True),
        ),
    ]
