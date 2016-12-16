# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0020_auto_20161216_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='pg_bene_sub',
            field=models.IntegerField(default=None, null=True, blank=True),
        ),
    ]
