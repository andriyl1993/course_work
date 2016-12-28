# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_scholluser_office'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='need_skills',
            field=models.ManyToManyField(related_name='need_skills', null=True, to='main.Skill', blank=True),
        ),
        migrations.AlterField(
            model_name='interview',
            name='skills',
            field=models.ManyToManyField(related_name='has_skills', null=True, to='main.Skill', blank=True),
        ),
    ]
