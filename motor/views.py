from django.http import HttpResponse
from django.shortcuts import render
from motor.serializers import FirstJobSerializer, JobSerializer
from motor.models import Job
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ValidationError


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
    serializer_class = JobSerializer

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

        except (Device.DoesNotExist, Job.DoesNotExist, KeyError, ValidationError) as error:
            pass            
            #logger.error("Error when updating Job status. Exception: {}".format(repr(error)))
        return HttpResponseNotFound("Unable to update job status.")

    def update(self, request, *args, **kwargs):
        # disable PUT requests - UpdateAPIView accepts them usually but we only want to accept PATCH requests.
        return HttpResponseNotAllowed(['PATCH'])

