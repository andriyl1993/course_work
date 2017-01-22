# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20161228_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='need_skills',
            field=models.ManyToManyField(related_name='need_skills', to='main.Skill', blank=True),
        ),
        migrations.AlterField(
            model_name='interview',
            name='skills',
            field=models.ManyToManyField(related_name='has_skills', to='main.Skill', blank=True),
        ),
    ]
