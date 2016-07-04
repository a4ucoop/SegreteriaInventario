# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0011_auto_20160616_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='bene',
            name='dt_registrazione_dg',
            field=models.IntegerField(default=None, verbose_name=b'anno di registrazione documento'),
        ),
    ]
