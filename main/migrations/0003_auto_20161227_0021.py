# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20161227_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholluser',
            name='car',
            field=models.ForeignKey(blank=True, to='main.Car', null=True),
        ),
    ]
