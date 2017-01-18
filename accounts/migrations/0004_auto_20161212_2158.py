# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-12 21:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20161212_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='active_begin',
            field=models.DateField(default=datetime.datetime(2016, 12, 12, 21, 58, 51, 523817)),
        ),
        migrations.AlterField(
            model_name='account',
            name='active_end',
            field=models.DateField(default=datetime.datetime(2017, 12, 13, 21, 58, 51, 523844)),
        ),
        migrations.AlterField(
            model_name='domainaccount',
            name='domain_active_begin',
            field=models.DateField(default=datetime.datetime(2016, 12, 12, 21, 58, 51, 529362)),
        ),
        migrations.AlterField(
            model_name='domainaccount',
            name='domain_active_end',
            field=models.DateField(default=datetime.datetime(2017, 12, 13, 21, 58, 51, 529401)),
        ),
        migrations.AlterField(
            model_name='jabberaccount',
            name='jabber_active_begin',
            field=models.DateField(default=datetime.datetime(2016, 12, 12, 21, 58, 51, 530545)),
        ),
        migrations.AlterField(
            model_name='jabberaccount',
            name='jabber_active_end',
            field=models.DateField(default=datetime.datetime(2017, 12, 13, 21, 58, 51, 530573)),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='mail_active_begin',
            field=models.DateField(default=datetime.datetime(2016, 12, 12, 21, 58, 51, 527284)),
        ),
        migrations.AlterField(
            model_name='mailaccount',
            name='mail_active_end',
            field=models.DateField(default=datetime.datetime(2017, 12, 13, 21, 58, 51, 527309)),
        ),
        migrations.AlterField(
            model_name='proxyaccount',
            name='proxy_active_begin',
            field=models.DateField(default=datetime.datetime(2016, 12, 12, 21, 58, 51, 525655)),
        ),
        migrations.AlterField(
            model_name='proxyaccount',
            name='proxy_active_end',
            field=models.DateField(default=datetime.datetime(2017, 12, 13, 21, 58, 51, 525680)),
        ),
    ]