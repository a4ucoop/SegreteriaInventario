# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventario', '0013_auto_20161012_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='inserito_da',
            field=models.ForeignKey(related_name='ricinv_inseritori', default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='possessore',
            field=models.ForeignKey(related_name='ricinv_possessori', default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
