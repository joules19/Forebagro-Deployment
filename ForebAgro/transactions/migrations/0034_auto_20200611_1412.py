# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-06-11 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0033_auto_20200610_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdebttransaction',
            name='initiator',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customerdebttransaction',
            name='updated_by',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='expensebasedtransaction',
            name='initiator',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='expensebasedtransaction',
            name='updated_by',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='forebdebttransaction',
            name='initiator',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='forebdebttransaction',
            name='updated_by',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='purchasetransaction',
            name='initiator',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='purchasetransaction',
            name='updated_by',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='salestransaction',
            name='initiator',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='salestransaction',
            name='updated_by',
            field=models.CharField(default='admin', max_length=20, null=True),
        ),
    ]
