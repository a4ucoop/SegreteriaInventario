# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccurateLocation',
            new_name='UbicazionePrecisa',
        ),
        migrations.RenameField(
            model_name='ubicazioneprecisa',
            old_name='location',
            new_name='ubicazione',
        ),
        migrations.AddField(
            model_name='item',
            name='ubicazione_precisa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='inventario.UbicazionePrecisa', null=True),
        ),
    ]
