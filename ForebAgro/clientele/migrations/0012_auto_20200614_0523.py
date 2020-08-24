# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-06-14 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientele', '0011_clientele_default_wallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientele',
            name='clientele_name',
            field=models.CharField(help_text='Clientele Name', max_length=100, unique=True),
        ),
    ]
