# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0024_auto_20161217_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ricognizioneinventariale',
            name='inventario',
        ),
    ]