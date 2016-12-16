# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0016_auto_20161215_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='inserito_da',
            field=models.ForeignKey(related_name='ricinv_inseritori', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
