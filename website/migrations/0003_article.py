# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20150418_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('link_text', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('summary', models.TextField()),
                ('plain_text', models.TextField()),
                ('relevance', models.IntegerField()),
                ('athlete', models.ForeignKey(to='website.Athlete')),
            ],
        ),
    ]
