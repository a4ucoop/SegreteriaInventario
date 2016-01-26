# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prova', '0003_item_residual_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.FileField(default=-1, upload_to=b'documents/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
