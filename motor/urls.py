from django.conf.urls import url, include
from django.contrib import admin
from motor.views import GetFirstJobView, UpdateJobStatusView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^first_job/$', csrf_exempt(GetFirstJobView.as_view()), name='api_get_first_job'),
	url(r'^job/(?P<job_id>\d*)/$', csrf_exempt(UpdateJobStatusView.as_view()), name='api_update_job_status'),
]
