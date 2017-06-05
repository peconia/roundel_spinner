from django.conf.urls import url
from motor.views import GetFirstJobView, UpdateJobStatusView, home, CreateNewJobView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^first_job/$', csrf_exempt(GetFirstJobView.as_view()), name='api_get_first_job'),
    url(r'^job/(?P<job_id>\d*)/$', csrf_exempt(UpdateJobStatusView.as_view()), name='api_update_job_status'),
    url(r'^$', home, name='home'),
    url(r'^job/(?P<job_type>\w+)', csrf_exempt(CreateNewJobView.as_view()), name='api_create_new_job'),
]
