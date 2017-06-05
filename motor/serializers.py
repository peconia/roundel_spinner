from rest_framework import serializers
from motor.models import Job


class FirstJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ('id', 'action')


class JobStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ('status',)


class JobTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ('action',)
