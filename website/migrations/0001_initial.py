# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


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
                ('age', models.FloatField()),
                ('height', models.CharField(max_length=10)),
                ('height_inches', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('draft_express_rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateField(auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.TextField()),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('relevance', models.IntegerField(default=0)),
                ('hash', models.CharField(max_length=64)),
                ('type', models.CharField(default=b'AR', max_length=2, choices=[(b'AR', b'Article'), (b'VI', b'Video'), (b'QU', b'quote')])),
                ('content', models.TextField()),
                ('plain_text', models.TextField()),
                ('modified', models.DateField(auto_now=True)),
                ('embed', models.CharField(max_length=500)),
                ('from_name', models.CharField(max_length=255)),
                ('athlete', models.ForeignKey(to='website.Athlete')),
            ],
        ),
    ]
