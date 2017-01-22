from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from models import SchollUser,Interview, Lesson, LEVELS, Skill, time_reg, Office, City, Car
from datetime import datetime, timedelta
from wrappers import check_access_right
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from serializers import SchollUserSerializer, OfficeSerializer, CarSerializer


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
        login = request.POST.get('username')
        password = request.POST.get('password')
        res = _login(request, login, password)
        if res == True:
            return redirect('/')
        elif 'req_fields' in res:
            return render(request, 'login.html', {'error': 'Fields are required'})
        else:
            return render(request, 'login.html', {'error': 'Invalid login data'})

def _login(request, username, password):
    user = authenticate(username=username, password=password)

    if not login or not password:
        return {'req_fields': True}

    if user:
        login(request, user)
        return True
    else:
        return False

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
        post_data = request.POST.copy()
        post_data = _register(post_data)
        if 'error_text' in post_data:
            return render(request, 'register.html', post_data)
        return redirect('/')

def _register(post_data):
    password = post_data.get('password')
    rep_password = post_data.get('rep_password')
    post_data['instructors'] = SchollUser.get_instructors()
    if SchollUser.objects.filter(username=post_data.get('username')):
        return post_data.update({'error_text': 'User already sign up'})
    if SchollUser.objects.filter(email=post_data.get('email')):
        return post_data.update({'error_text': 'Email already sign up'})
    if password != rep_password:
        return post_data.update({'error_text': 'Passwords not equeal'})
    if len(password) < 6:
        return post_data.update({'error_text': 'Password\'s minumal length 6 symbols'})
    user = SchollUser.objects.create_user(
        username=post_data.get('username'),
        password=post_data.get('password'),
        email=post_data.get('email'),
    )
    user.role = 'client'
    user.is_many_lessons = True
    user.save()
    datetime_start = post_data.get('interview_date')
    datetime_end = datetime.strptime(datetime_start, time_reg) + timedelta(hours=1)
    interview = Interview(
        start=datetime_start,
        end=datetime_end.strftime(time_reg),
        student=user,
    )
    interview.instructor = Interview.objects.filter(id=int(post_data.get("instructor"))) if post_data.get(
        "instructor") else None
    interview.save()
    return []

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
    city_id = request.GET.get('city')
    offices = _offices(city_id)
    return render(request, "offices.html", {'cities': City.objects.filter(id = int(city_id)), 'offices': offices})

def _offices(city_id):
    if city_id:
        offices = Office.objects.filter(city__id=city_id)
    else:
        offices = Office.objects.all()
    return offices

@login_required
@check_access_right(['director', 'manager'])
def count_workers_view(request):
    offices = Office.objects.all()
    return render(request, "count_workers.html", {'offices': offices})


@login_required
@check_access_right(['director', 'manager'])
def count_clients_view(request):
    cities = _count_clients()
    return render(request, "count_clients.html", {'cities': cities})

def _count_clients():
    return SchollUser.objects.filter(role='client').count()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request),
        'offices': reverse('office-list', request=request),
        'car': reverse('car-list', request=request),
        'count-clients': reverse('client-count', request=request),
        'signup': reverse('api_signup', request=request),
        'login': reverse('api_login', request=request),
    })

@api_view(['GET'])
@check_access_right(['director', 'manager'])
def api_count_clients(request, format=None):
    return Response({
        'clients': _count_clients(),
    })

@api_view(['GET'])
@check_access_right(['director', 'manager'])
def api_offices(request, id):
    offices = _offices(id)
    serializer = OfficeSerializer(offices, many=True)
    return Response({
        'offices': serializer.data,
    })

@api_view(['POST'])
def api_register(request):
    post_data = request.POST.copy()
    res_data = _register(post_data)
    if 'error_text' in res_data:
        resp = res_data
    else:
        resp = {'result': True}
    return Response(resp)

@api_view(['POST'])
def api_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    res = _login(request, username, password)
    request.session['username'] = username
    request.session['password'] = password
    school_user = SchollUser.objects.filter(user_ptr = request.user)
    if res == True:
        return Response(
            {
                'result': True,
                'username': username,
                'role': school_user.role if school_user else "",
            }
        )
    elif 'req_fields' in res:
        return Response({'result': False, 'error': 'Fields are required'})
    else:
        return Response({'result': False, 'error': 'Invalid login data'})

@api_view(['POST'])
def api_logout(request):
    logout(request)
    return Response({'result': True})

class OfficeList(generics.ListAPIView):
    queryset = Office.objects.all()
    model = Office
    serializer_class = OfficeSerializer

class CarList(generics.ListAPIView):
    queryset = Car.objects.all()
    model = Car
    serializer_class = CarSerializer

class OfficeDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Office
    serializer_class = OfficeSerializer

class SchollUserList(generics.ListAPIView):
    queryset = SchollUser.objects.all()
    model = SchollUser
    serializer_class = SchollUserSerializer

class SchollUserDetail(generics.ListAPIView):
    queryset = SchollUser.objects.all()
    model = SchollUser
    serializer_class = SchollUserSerializer