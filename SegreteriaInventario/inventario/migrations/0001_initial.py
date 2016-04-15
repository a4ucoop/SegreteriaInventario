# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccurateLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cd_invent', models.CharField(max_length=8)),
                ('pg_bene', models.IntegerField(default=None)),
                ('pg_bene_sub', models.IntegerField(default=None)),
                ('ds_bene', models.CharField(max_length=400)),
                ('dt_registrazione_buono', models.DateTimeField(verbose_name=b'data registrazione buono')),
                ('cd_categ_gruppo', models.CharField(max_length=60)),
                ('ds_categ_gruppo', models.CharField(max_length=255)),
                ('ds_spazio', models.CharField(max_length=2000)),
                ('dt_ini_ammortamento', models.DateTimeField(verbose_name=b'data inizio ammortamento')),
                ('valore_convenzionale', models.DecimalField(max_digits=15, decimal_places=2)),
                ('valore_residuo', models.DecimalField(max_digits=15, decimal_places=2)),
                ('immagine', models.FileField(null=True, upload_to=b'pictures/%Y/%m/%d')),
            ],
        ),
    ]
