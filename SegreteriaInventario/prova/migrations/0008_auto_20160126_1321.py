# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prova', '0007_auto_20151129_0049'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccurateLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=2000)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='accurate_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='prova.AccurateLocation', null=True),
        ),
    ]
