# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20161228_0549'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholluser',
            name='phone',
            field=models.CharField(default='', max_length=14),
            preserve_default=False,
        ),
    ]
