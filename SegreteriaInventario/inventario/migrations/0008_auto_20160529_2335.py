# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_auto_20160529_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bene',
            name='num_doc_rif',
            field=models.CharField(default=None, max_length=128),
        ),
    ]
