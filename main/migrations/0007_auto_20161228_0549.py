# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20161227_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baselesson',
            name='end',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
