# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseLesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=31)),
                ('number', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('teor_part_mark', models.FloatField()),
                ('practice_part_mark', models.FloatField()),
                ('is_passed', models.BooleanField(default=False)),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QualityList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now=True)),
                ('total_mark', models.IntegerField()),
                ('car', models.ForeignKey(to='main.Car')),
            ],
        ),
        migrations.CreateModel(
            name='QualityRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
                ('mark', models.IntegerField()),
                ('note', models.TextField()),
                ('quality_list', models.ForeignKey(to='main.QualityList')),
            ],
        ),
        migrations.CreateModel(
            name='SchollUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(max_length=15, choices=[(b'director', b'Director'), (b'alternate', b'Alternate'), (b'hr_head', b'Head of HR'), (b'manager', b'Manager'), (b'instr_head', b'Instructor Head'), (b'instructor', b'Simple instructor'), (b'personal', b'Personal'), (b'client', b'Client')])),
                ('student_level', models.IntegerField(default=0, choices=[(0, b'Begginer'), (1, b'Medium'), (2, b'Strong'), (3, b'Professional')])),
                ('about', models.TextField()),
                ('is_many_lessons', models.BooleanField(default=False)),
                ('car', models.ForeignKey(to='main.Car')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name='TravelList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instructor', models.ForeignKey(to='main.SchollUser')),
            ],
        ),
        migrations.CreateModel(
            name='TravelListRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('reason', models.TextField()),
                ('end', models.DateTimeField()),
                ('distance', models.FloatField()),
                ('travel_list', models.ForeignKey(to='main.TravelList')),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('baselesson_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.BaseLesson')),
                ('need_skills', models.ManyToManyField(related_name='need_skills', to='main.Skill')),
                ('skills', models.ManyToManyField(related_name='has_skills', to='main.Skill')),
            ],
            bases=('main.baselesson',),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('baselesson_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='main.BaseLesson')),
                ('distance_travel_with', models.FloatField(default=0)),
                ('distance_travel_without', models.FloatField(default=0)),
                ('is_add', models.BooleanField(default=False)),
                ('new_skills', models.ManyToManyField(related_name='new_skills', to='main.Skill')),
            ],
            bases=('main.baselesson',),
        ),
        migrations.AddField(
            model_name='exam',
            name='user',
            field=models.ForeignKey(to='main.SchollUser'),
        ),
        migrations.AddField(
            model_name='baselesson',
            name='instructor',
            field=models.ForeignKey(related_name='user_instructor', to='main.SchollUser'),
        ),
        migrations.AddField(
            model_name='baselesson',
            name='student',
            field=models.ForeignKey(related_name='user_student', to='main.SchollUser'),
        ),
    ]
