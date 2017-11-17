# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='name', max_length=64)),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'accounts',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BalanceCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name='date', default=django.utils.timezone.now)),
                ('real', models.DecimalField(verbose_name='real balance', decimal_places=3, max_digits=12)),
                ('account', models.ForeignKey(verbose_name='account', to='accountancy.Account')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name='date', default=django.utils.timezone.now)),
                ('counterparty', models.CharField(verbose_name='counterparty', null=True, blank=True, max_length=64)),
                ('account', models.ForeignKey(verbose_name='account', to='accountancy.Account')),
            ],
            options={
                'verbose_name': 'bill',
                'verbose_name_plural': 'bills',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='name', max_length=64)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, verbose_name='code', max_length=3)),
            ],
            options={
                'verbose_name': 'currency',
                'verbose_name_plural': 'currencies',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=64)),
                ('comment', models.CharField(verbose_name='comment', null=True, blank=True, max_length=128)),
                ('amount', models.DecimalField(verbose_name='amount', default=1, decimal_places=3, max_digits=12)),
                ('unit_price', models.DecimalField(verbose_name='unit price', decimal_places=3, max_digits=12)),
                ('bill', models.ForeignKey(verbose_name='bill', to='accountancy.Bill')),
                ('category', models.ForeignKey(verbose_name='category', null=True, to='accountancy.Category', blank=True)),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clazz', models.CharField(verbose_name='class', max_length=64)),
                ('brand', models.CharField(verbose_name='brand', null=True, blank=True, max_length=64)),
                ('name', models.CharField(verbose_name='name', max_length=64)),
                ('comment', models.CharField(verbose_name='comment', null=True, blank=True, max_length=128)),
                ('size', models.DecimalField(verbose_name='size', decimal_places=3, null=True, blank=True, max_digits=12)),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbr', models.CharField(unique=True, verbose_name='abbreviation', max_length=16)),
            ],
            options={
                'verbose_name': 'unit',
                'verbose_name_plural': 'units',
                'ordering': ['abbr'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(verbose_name='unit', null=True, to='accountancy.Unit', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(verbose_name='product', null=True, to='accountancy.Product', blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.ForeignKey(verbose_name='unit', null=True, to='accountancy.Unit', blank=True),
        ),
        migrations.AddField(
            model_name='account',
            name='currency',
            field=models.ForeignKey(verbose_name='currency', to='accountancy.Currency'),
        ),
    ]
