# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20161227_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='place',
            field=models.CharField(default='', max_length=63),
            preserve_default=False,
        ),
    ]
