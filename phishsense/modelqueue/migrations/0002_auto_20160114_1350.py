# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-14 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelqueue', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phishverdictmodel',
            name='url_sha',
        ),
        migrations.AddField(
            model_name='investigateurlmodel',
            name='url_sha',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
