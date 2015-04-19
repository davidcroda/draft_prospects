# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='hash',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
    ]
