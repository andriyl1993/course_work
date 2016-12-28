from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from main.views import index_view, login_view, logout_view, register_view, lesson_view, set_interview_results, set_lesson_result, \
    managers_view, offices_view, count_workers_view, count_clients_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index_view, name="index"),
    url(r'^login/', login_view, name="login"),
    url(r'^logout/', logout_view, name="logout"),
    url(r'^register/', register_view, name="register"),
    url(r'^lesson/', lesson_view, name="lesson"),
    url(r'^interview-result/', set_interview_results, name="interview-result"),
    url(r'^lesson-result/', set_lesson_result, name="lesson-result"),
    url(r'^managers/', managers_view, name="managers"),
    url(r'^offices/', offices_view, name="offices"),
    url(r'^count-workers/', count_workers_view, name="count-workes"),
    url(r'^count-clients/', count_clients_view, name="count-clients"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
