# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prova', '0004_item_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='image',
            new_name='picture',
        ),
    ]
