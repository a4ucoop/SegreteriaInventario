# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0014_auto_20161025_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Esse3User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='ricognizioneinventariale',
            name='possessore',
            field=models.ForeignKey(related_name='ricinv_possessori', default=None, to='inventario.Esse3User'),
        ),
    ]
