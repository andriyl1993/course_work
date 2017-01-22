from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns

from main.views import index_view, login_view, logout_view, register_view, lesson_view, set_interview_results, set_lesson_result, \
    managers_view, offices_view, count_workers_view, count_clients_view

from main.views import api_root, SchollUserList, OfficeDetail, OfficeList, CarList, api_count_clients, api_offices, \
    api_register, api_login, api_logout

urlpatterns = patterns('',
    url(r'api/$', api_root, name='api_root'),
    url(r'api/office-list/$', OfficeList.as_view(), name="office-list"),
    url(r'api/office-detail/(?P<pk>\d+)/$', OfficeDetail.as_view(), name="office-detail"),
    url(r'api/car-list/$', CarList.as_view(), name="car-list"),
    url(r'api/users-list/$', SchollUserList.as_view(), name="user-list"),
    url(r'api/count-clients/$', api_count_clients, name="client-count"),
    url(r'api/city-offices/(?P<id>\d+)/$', api_offices, name="city-offices"),
    url(r'api/signup/$', api_register, name="api_signup"),
    url(r'api/login/$', api_login, name="api_login"),
    url(r'api/logout/$', api_logout, name="api_logout"),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns('',
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
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
)