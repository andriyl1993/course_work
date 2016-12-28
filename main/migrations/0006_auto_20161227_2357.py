# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_lesson_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='place',
            field=models.CharField(max_length=63, null=True, blank=True),
        ),
    ]
