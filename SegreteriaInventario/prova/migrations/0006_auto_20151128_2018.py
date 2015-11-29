# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prova', '0005_auto_20151128_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='picture',
            field=models.FileField(upload_to=b'pictures/%Y/%m/%d'),
        ),
    ]
