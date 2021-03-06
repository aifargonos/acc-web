# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 18:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('accountancy', '0001_initial'), ('accountancy', '0002_account_owner'), ('accountancy', '0003_account_owner_remove_default')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name_plural': 'accounts',
                'verbose_name': 'account',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BalanceCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
                ('real', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='real balance')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountancy.Account', verbose_name='account')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')),
                ('counterparty', models.CharField(blank=True, max_length=64, null=True, verbose_name='counterparty')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountancy.Account', verbose_name='account')),
            ],
            options={
                'verbose_name_plural': 'bills',
                'verbose_name': 'bill',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True, verbose_name='code')),
            ],
            options={
                'verbose_name_plural': 'currencies',
                'verbose_name': 'currency',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('comment', models.CharField(blank=True, max_length=128, null=True, verbose_name='comment')),
                ('amount', models.DecimalField(decimal_places=3, default=1, max_digits=12, verbose_name='amount')),
                ('unit_price', models.DecimalField(decimal_places=3, max_digits=12, verbose_name='unit price')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountancy.Bill', verbose_name='bill')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accountancy.Category', verbose_name='category')),
            ],
            options={
                'verbose_name_plural': 'items',
                'verbose_name': 'item',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clazz', models.CharField(max_length=64, verbose_name='class')),
                ('brand', models.CharField(blank=True, max_length=64, null=True, verbose_name='brand')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('comment', models.CharField(blank=True, max_length=128, null=True, verbose_name='comment')),
                ('size', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, verbose_name='size')),
            ],
            options={
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbr', models.CharField(max_length=16, unique=True, verbose_name='abbreviation')),
            ],
            options={
                'verbose_name_plural': 'units',
                'verbose_name': 'unit',
                'ordering': ['abbr'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accountancy.Unit', verbose_name='unit'),
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accountancy.Product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accountancy.Unit', verbose_name='unit'),
        ),
        migrations.AddField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountancy.Currency', verbose_name='currency'),
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='owner'),
        ),
    ]
