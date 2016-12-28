# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20161227_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baselesson',
            name='instructor',
            field=models.ForeignKey(related_name='user_instructor', blank=True, to='main.SchollUser', null=True),
        ),
    ]
