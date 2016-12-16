# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0018_auto_20161215_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='nuovo_possessore',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
