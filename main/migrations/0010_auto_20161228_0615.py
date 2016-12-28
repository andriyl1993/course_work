# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20161228_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholluser',
            name='phone',
            field=models.CharField(max_length=14, null=True, blank=True),
        ),
    ]
