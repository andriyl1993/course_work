# -*- coding: utf-8 -*-

from models import City, Office, Car, SchollUser, Skill, Interview, Lesson, TravelList, TravelListRow, \
    QualityList, QualityRow, Exam
from rest_framework import serializers


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class OfficeSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Office
        fields = ('name', 'city')


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'name', 'number')


class SchollUserSerializer(serializers.HyperlinkedModelSerializer):
    office = OfficeSerializer()
    car = CarSerializer()

    class Meta:
        model = SchollUser
        fields = ('username', 'first_name', 'last_name', 'role', 'student_level', 'about', 'is_many_lessons', 'car', 'phone', 'office')


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ('name')


class InterviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interview
        fields = ('skills', 'need_skills','start', 'end', 'instructor', 'student', 'price')


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ('new_skills', 'distance_travel_with','distance_travel_without', 'start', 'end', 'instructor', 'student', 'price')
