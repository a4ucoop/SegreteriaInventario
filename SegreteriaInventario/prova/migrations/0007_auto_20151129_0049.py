# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prova', '0006_auto_20151128_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='picture',
            field=models.FileField(null=True, upload_to=b'pictures/%Y/%m/%d'),
        ),
    ]
