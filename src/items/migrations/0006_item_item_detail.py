# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 05:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20180103_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_detail',
            field=models.TextField(blank=True, help_text='seperate each item by comma', null=True),
        ),
    ]
