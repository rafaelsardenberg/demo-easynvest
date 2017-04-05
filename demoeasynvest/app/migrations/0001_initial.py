# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operacao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('categoria', models.CharField(max_length=255)),
                ('acao', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mes', models.CharField(max_length=255)),
                ('ano', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Valor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacao_id', models.IntegerField(default=0)),
                ('periodo_id', models.IntegerField(default=0)),
                ('quantidade', models.CharField(max_length=255)),
            ],
        ),
    ]