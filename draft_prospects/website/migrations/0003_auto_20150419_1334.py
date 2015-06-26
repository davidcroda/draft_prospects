# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_entity_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='athlete',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='athlete',
            name='last_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entity',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
