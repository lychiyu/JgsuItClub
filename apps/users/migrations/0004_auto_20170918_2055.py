# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-09-18 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userenroll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userenroll',
            name='status',
            field=models.CharField(choices=[('0', '\u672a\u5904\u7406'), ('1', '\u672a\u901a\u8fc7'), ('2', '\u5df2\u901a\u8fc7')], default=0, max_length=1, verbose_name='\u5ba1\u6838\u72b6\u6001'),
        ),
    ]
