# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_scholluser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholluser',
            name='about',
            field=models.TextField(null=True, blank=True),
        ),
    ]
