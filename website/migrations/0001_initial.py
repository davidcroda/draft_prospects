# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('school', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('height', models.CharField(max_length=10)),
                ('height_inches', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('draft_express_rank', models.IntegerField()),
            ],
        ),
    ]
