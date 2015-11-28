# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prova', '0002_item_item_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='residual_value',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=2),
            preserve_default=False,
        ),
    ]
