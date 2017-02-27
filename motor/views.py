from django.http import HttpResponse
from django.shortcuts import render
from motor.serializers import FirstJobSerializer
from motor.models import Job
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


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

