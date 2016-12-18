# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0023_auto_20161217_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cd_invent', models.CharField(max_length=8)),
                ('ds_invent', models.CharField(max_length=256)),
            ],
        ),
        migrations.RemoveField(
            model_name='ricognizioneinventariale',
            name='cd_invent',
        ),
        migrations.RemoveField(
            model_name='ricognizioneinventariale',
            name='ds_invent',
        ),
        migrations.AddField(
            model_name='ricognizioneinventariale',
            name='inventario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='inventario.Inventario', null=True),
        ),
    ]
