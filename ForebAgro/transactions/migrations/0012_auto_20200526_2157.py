# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-05-26 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_auto_20200518_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdebttransaction',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='forebdebttransaction',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='purchasetransaction',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='salestransaction',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
