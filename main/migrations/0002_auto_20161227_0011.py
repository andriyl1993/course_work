# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholluser',
            name='car',
            field=models.ForeignKey(to='main.Car', blank=True),
        ),
    ]
