# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-06-07 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constants',
            name='constant_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
