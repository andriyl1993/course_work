from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from models import SchollUser,Interview, Lesson, LEVELS, Skill, time_reg, Office, City
from datetime import datetime, timedelta
from wrappers import check_access_right
from django.contrib.auth.decorators import login_required


def index_view(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return render(request, 'index.html')
        else:
            return redirect('/login/')
    else:
        raise Exception("POST")


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return redirect('/')
        else:
            return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error': 'Fields are required'})

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid login data'})


@login_required
def logout_view(request):
    if request.method == "GET":
        logout(request)
        return render(request, 'login.html')
    else:
        return redirect('/')


def register_view(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return redirect('/')
        else:
            return render(request, 'register.html', {'instructors': SchollUser.get_instructors()})
    else:
        password = request.POST.get('password')
        rep_password = request.POST.get('rep_password')

        post_data = request.POST.copy()
        post_data['instructors'] = SchollUser.get_instructors()
        if SchollUser.objects.filter(username=post_data.get('username')):
            return render(request, 'register.html', post_data.update({'error_text': 'User already sign up'}))
        if SchollUser.objects.filter(email=post_data.get('email')):
            post_data['error_text'] = 'Email already sign up'
            return render(request, 'register.html', post_data)
        if password != rep_password:
            return render(request, 'register.html', post_data.update({'error_text': 'Passwords not equeal'}))
        if len(password) < 6:
            return render(request, 'register.html', post_data.update({'error_text': 'Password\'s minumal length 6 symbols'}))
        user = SchollUser.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
        )
        user.role='client'
        user.is_many_lessons = True
        user.save()
        datetime_start = request.POST.get('interview_date')
        datetime_end = datetime.strptime(datetime_start, time_reg) + timedelta(hours=1)
        interview = Interview(
            start=datetime_start,
            end=datetime_end.strftime(time_reg),
            student=user,
        )
        interview.instructor = Interview.objects.filter(id=int(post_data.get("instructor"))) if post_data.get("instructor") else None
        interview.save()
        return redirect('/')

@login_required
@check_access_right(['client'])
def lesson_view(request):
    if request.method == "GET":
        instructors = SchollUser.get_instructors()
        return render(request, "lesson.html", {'instructors': instructors})
    else:
        if datetime.strptime(request.POST.get('start'), time_reg).hour < 8:
            return render(request, "lesson.html", {'error_text': 'Early'})
        if datetime.strptime(request.POST.get('start'), time_reg).hour > 19:
            return render(request, "lesson.html", {'error_text': 'Later'})

        lesson = Lesson(
            start=request.POST.get('start'),
            place=request.POST.get('place'),
            student=request.user.scholluser
        )
        lesson.save()
        return redirect('/')

@login_required
@check_access_right(['instr_head', 'instructor'])
def set_interview_results(request):
    if request.method == "GET":
        students = SchollUser.objects.filter(role='client')
        return render(request, 'interview_results.html', {'students': students, 'levels': LEVELS})
    else:
        student = SchollUser.objects.get(id=request.POST.get('student'))
        interview = Interview.objects.get(student=student)
        if interview:
            interview.end = datetime.now()
            interview.price = 100
            interview.skills = map(lambda x: Skill.objects.get_or_create(name=x.strip())[0],request.POST.get('have_skills').split(','))
            interview.need_skills = map(lambda x: Skill.objects.get_or_create(name=x.strip())[0],request.POST.get('need_skills').split(','))
            interview.save()
            student.student_level = int(request.POST.get('level'))
            student.save()
        return redirect('/')

@login_required
@check_access_right(['instr_head', 'instructor'])
def set_lesson_result(request):
    if request.method == "GET":
        lessons = Lesson.get_today_lessons()
        return render(request, 'lesson_result.html', {'lessons': lessons})
    else:
        post_data = request.POST
        if post_data.get('lesson'):
            lesson = Lesson.objects.get(id=post_data.get('lesson'))
            lesson.new_skills = map(lambda x: Skill.objects.get_or_create(name=x.strip())[0],request.POST.get('new_skills').split(','))
            lesson.distance_travel_with = post_data.get('distance_travel_with')
            lesson.distance_travel_without = post_data.get('distance_travel_without')
            lesson.end = datetime.now()
            lesson.save()
            return redirect('/')
        return redirect('/')

@login_required
@check_access_right(['director', 'alternate'])
def managers_view(request):
    managers = SchollUser.objects.filter(role='manager')
    return render(request, "managers.html", {"managers": managers})


@login_required
@check_access_right(['director', 'alternate'])
def offices_view(request):
    cities = City.objects.all()
    offices = []

    if request.GET.get('city'):
        city = City.objects.get(id = int(request.GET.get('city')))
        offices = Office.objects.filter(city = city)
    return render(request, "offices.html", {'cities': cities, 'offices': offices})


@login_required
@check_access_right(['director', 'manager'])
def count_workers_view(request):
    offices = Office.objects.all()
    return render(request, "count_workers.html", {'offices': offices})


@login_required
@check_access_right(['director', 'manager'])
def count_clients_view(request):
    cities = City.objects.all()
    return render(request, "count_clients.html", {'cities': cities})