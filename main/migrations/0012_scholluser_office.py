# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_city_office'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholluser',
            name='office',
            field=models.ForeignKey(blank=True, to='main.Office', null=True),
        ),
    ]
