# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=400)),
                ('purchase_date', models.DateTimeField(verbose_name=b'purchase date')),
                ('price', models.DecimalField(max_digits=12, decimal_places=2)),
                ('location', models.CharField(max_length=2000)),
                ('depreciation_starting_date', models.DateTimeField(verbose_name=b'depreciation starting date')),
            ],
        ),
    ]
