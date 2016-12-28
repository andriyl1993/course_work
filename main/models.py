# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

time_reg = "%Y-%m-%d %H:%M:%S"

LEVELS = (
    (0, 'Begginer'),
    (1, 'Medium'),
    (2, 'Strong'),
    (3, 'Professional'),
)


class City(models.Model):
    name = models.CharField(max_length=31)

    def __unicode__(self):
        return self.name

    def get_count_clients(self):
        offices = Office.objects.filter(city = self)
        instructors = SchollUser.objects.filter(role__in = ['instructor', 'instr_head'], office__in = offices)
        return reduce(lambda res, inst: res + inst.get_students_of_instructor(), instructors, 0)


class Office(models.Model):
    name = models.CharField(max_length=63)
    city = models.ForeignKey(City)

    def __unicode__(self):
        return self.name

    def get_count_workes(self):
        return SchollUser.objects.filter(office = self).count()

class Car(models.Model):
    name = models.CharField(max_length=31)
    number = models.CharField(max_length=7)


class SchollUser(User):
    role = models.CharField(
        max_length=15,
        choices=(
            ('director', 'Director'),
            ('alternate', 'Alternate'),
            ('hr_head', 'Head of HR'),
            ('manager', 'Manager'),
            ('instr_head', 'Instructor Head'),
            ('instructor', 'Simple instructor'),
            ('personal', 'Personal'),
            ('client', 'Client'),
        )
    )
    student_level = models.IntegerField(
        default=0,
        choices=LEVELS
    )
    about = models.TextField(blank=True, null=True)
    is_many_lessons = models.BooleanField(default=False)
    car = models.ForeignKey(Car, blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    office = models.ForeignKey(Office, null=True, blank=True)

    @staticmethod
    def get_instructors():
        return SchollUser.objects.filter(role__in=['instructor', 'instr_head'])

    def get_students_of_instructor(self):
        return Interview.objects.filter(instructor=self).count()


class Skill(models.Model):
    name = models.CharField(max_length=31)

    def __unicode__(self):
        return self.name


class BaseLesson(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    instructor = models.ForeignKey(SchollUser, related_name="user_instructor",blank=True, null=True)
    student = models.ForeignKey(SchollUser, related_name="user_student")
    price = models.FloatField()

    def set_price(self):
        self.price = 100
        return self.price

    def get_free_instructor(self):
        all_instructors = SchollUser.get_instructors()
        return all_instructors[0] if all_instructors else None

    def save(self, *args, **kwargs):
        self.set_price()
        super(BaseLesson, self).save(*args, **kwargs)

class Interview(BaseLesson):
    skills = models.ManyToManyField(Skill, related_name="has_skills", blank=True)
    need_skills = models.ManyToManyField(Skill, related_name="need_skills", blank=True)

    def save(self, *args, **kwargs):
        self.instructor = self.get_free_instructor()
        super(Interview, self).save(*args, **kwargs)


class Lesson(BaseLesson):
    new_skills = models.ManyToManyField(Skill, related_name="new_skills")
    distance_travel_with = models.FloatField(default=0)
    distance_travel_without = models.FloatField(default=0)
    is_add = models.BooleanField(default=False)
    place = models.CharField(max_length=63, blank=True, null=True)

    def set_instructor(self, new_instructor, user=None):
        if self.instructor:
            return self.instructor

        if new_instructor:
            self.instructor = SchollUser.objects.get(id=int(new_instructor))
        else:
            lessons = Lesson.objects.filter(student=user if user else self.user).order_by('-start')
            self.instructor = lessons[0].instructor if lessons else None
        return self.instructor

    def is_additional(self):
        if self.student:
            exam = Exam.objects.filter(user=self.student)
            self.is_add = True if exam else False
        return self.is_add

    @staticmethod
    def get_today_lessons():
        print datetime.today(), datetime.today() + timedelta(days=1)
        return Lesson.objects.filter(start__range=[datetime.today(), datetime.today() + timedelta(days=1)])

    def __unicode__(self):
        return "%s - %s" % (self.student.username, self.start.strftime(time_reg))

    def save(self, *args, **kwargs):
        super(Lesson, self).save(*args, **kwargs)
        instructor = self.get_free_instructor() if not self.instructor else self.instructor
        self.set_instructor(instructor.id)
        self.is_additional()
        super(Lesson, self).save(*args, **kwargs)

class TravelList(models.Model):
    instructor = models.ForeignKey(SchollUser)


class TravelListRow(models.Model):
    start = models.DateTimeField()
    travel_list = models.ForeignKey(TravelList)
    reason = models.TextField()
    end = models.DateTimeField()
    distance = models.FloatField()


class QualityList(models.Model):
    date = models.DateField(auto_now=True)
    car = models.ForeignKey(Car)
    total_mark = models.IntegerField()


class QualityRow(models.Model):
    name = models.CharField(max_length=127)
    mark = models.IntegerField()
    note = models.TextField()
    quality_list = models.ForeignKey(QualityList)


class Exam(models.Model):
    date = models.DateField()
    user = models.ForeignKey(SchollUser)
    teor_part_mark = models.FloatField()
    practice_part_mark = models.FloatField()
    is_passed = models.BooleanField(default=False)
    note = models.TextField()

