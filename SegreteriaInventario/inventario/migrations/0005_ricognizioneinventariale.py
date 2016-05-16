# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_bene_id_bene'),
    ]

    operations = [
        migrations.CreateModel(
            name='RicognizioneInventariale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cd_invent', models.CharField(max_length=8)),
                ('pg_bene', models.IntegerField(default=None)),
                ('pg_bene_sub', models.IntegerField(default=None)),
                ('ds_spazio', models.CharField(max_length=2000, null=True)),
                ('immagine', models.FileField(null=True, upload_to=b'pictures/%Y/%m/%d', blank=True)),
                ('ubicazione_precisa', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='inventario.UbicazionePrecisa', null=True)),
            ],
        ),
    ]
