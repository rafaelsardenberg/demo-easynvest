# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170404_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='titulo',
            name='acao',
        ),
        migrations.AddField(
            model_name='operacao',
            name='acao',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
