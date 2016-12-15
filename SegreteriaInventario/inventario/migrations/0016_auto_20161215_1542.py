# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0015_auto_20161026_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='possessore',
            field=models.CharField(max_length=100),
        ),
    ]
