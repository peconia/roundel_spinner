from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import render
from motor.serializers import FirstJobSerializer, JobStatusSerializer, JobTypeSerializer
from motor.models import Job
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.core.exceptions import ValidationError
from django.contrib import messages


def home(request):   
    return render(request, 'motor/home.html', {})


class GetFirstJobView(generics.RetrieveAPIView):
    """
    Get the first available job to process.
    Returns HTTP 200 with Job Id, Action and Script for the earliest pending job.
    Returns HTTP 200 with message NO PENDING JOB if d there are no pending jobs.

    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = FirstJobSerializer

    def get(self, request, *args, **kwargs):

        try:
            job = Job.objects.filter(status=Job.Pending).earliest('created')
            serializer = self.get_serializer(job)
            return Response(serializer.data)

        except Job.DoesNotExist:
            return HttpResponse("NO PENDING JOB")


class UpdateJobStatusView(generics.UpdateAPIView):
    """
    Update a Job instance to have the new status as reported by the RPi.
    Requires a PATCH request.
    Returns HTTP 200 if update was successful, otherwise 404.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = JobStatusSerializer

    def partial_update(self, request, *args, **kwargs): 
        try:
            status = request.data['status']
            timestamp = request.data['timestamp']
            if not timestamp.endswith("Z"):
                timestamp = "%sZ" % timestamp

            job = Job.objects.get(id=kwargs['job_id'])
            serializer = self.get_serializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                job.status = status
                job.status_updated_time = timestamp
                job.save()
                return HttpResponse("UPDATE SUCCESSFUL")
            else:
                pass
                #logger.info("Update job request had invalid data.")

        except (Job.DoesNotExist, KeyError, ValidationError) as error:
            pass            
            #logger.error("Error when updating Job status. Exception: {}".format(repr(error)))
        return HttpResponseNotFound("Unable to update job status.")

    def update(self, request, *args, **kwargs):
        # disable PUT requests - UpdateAPIView accepts them usually but we only want to accept PATCH requests.
        return HttpResponseNotAllowed(['PATCH'])


class CreateNewJobView(generics.CreateAPIView):
    """
    Create a new job for the Rpi
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = JobTypeSerializer

    def create(self, request, *args, **kwargs):
        try:
            job_type = kwargs["job_type"].upper()

            if job_type in [i[0] for i in Job.Actions]:

                # check if reset job already pending
                if len(Job.objects.filter(action=job_type, status=Job.Pending)) > 0:
                    messages.warning(request._request, "Job already pending.")
                    return HttpResponse("{} job already pending.".format(job_type))
                Job.objects.create(action=job_type)
                messages.success(request._request, "{} job created successfully.".format(job_type))
                return HttpResponse("{} job created successfully.".format(job_type),)
            else:
                return HttpResponseNotFound("NO SUCH JOB TYPE")
        except KeyError as ex:
            # logger.error("Error creating new job. Exception {}".format(repr(ex)))
            return HttpResponseNotFound("Unable to create new job.")
