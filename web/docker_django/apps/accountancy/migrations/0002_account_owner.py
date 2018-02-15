# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 17:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accountancy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(default='aifargonos', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='owner'),
        ),
    ]