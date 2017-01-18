# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 16:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='active_begin',
            field=models.DateField(default=datetime.datetime(2016, 3, 14, 16, 10, 51, 712875)),
        ),
        migrations.AlterField(
            model_name='account',
            name='active_end',
            field=models.DateField(default=datetime.datetime(2017, 3, 15, 16, 10, 51, 712900)),
        ),
        migrations.AlterField(
            model_name='domainaccount',
            name='domain_active_begin',
            field=models.DateField(default=datetime.datetime(2016, 3, 14, 16, 10, 51, 717690)),
        ),
        migrations.AlterField(
            model_name='domainaccount',
            name='domain_active_end',
            field=models.DateField(default=datetime.datetime(2017, 3, 15, 16, 10, 51, 717709)),
        ),
        migrations.AlterField(
            model_name='jabberaccount',
            name='jabber_active_begin',
            field=models.DateField(default=datetime.datetime(2016, 3, 14, 16, 10, 51, 718499)),
        ),
        migrations.AlterField(
            model_name='jabberaccount',
            name='jabber_active_end',
            field=models.DateField(default=datetime.datetime(2017, 3, 15, 16, 10, 51, 718515)),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='mail_active_begin',
            field=models.DateField(default=datetime.datetime(2016, 3, 14, 16, 10, 51, 715925)),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='mail_active_end',
            field=models.DateField(default=datetime.datetime(2017, 3, 15, 16, 10, 51, 715941)),
        ),
        migrations.AlterField(
            model_name='proxyaccount',
            name='proxy_active_begin',
            field=models.DateField(default=datetime.datetime(2016, 3, 14, 16, 10, 51, 714565)),
        ),
        migrations.AlterField(
            model_name='proxyaccount',
            name='proxy_active_end',
            field=models.DateField(default=datetime.datetime(2017, 3, 15, 16, 10, 51, 714584)),
        ),
    ]
