from django.db import models
from django.utils import timezone


class Job(models.Model):

    Spin_clockwise = 'CLOCKWISE'
    Spin_counterclockwise = 'COUNTER_CLOCKWISE'
    Actions = ((Spin_clockwise, "Spin Clockwise"),
               (Spin_counterclockwise, "Spin Counterclockwise"),
               )

    Pending = 0
    Accepted = 1
    Done = 2
    Failed = 3
    Statuses = ((Pending, "Pending"),
                (Accepted, "Accepted"),
                (Done, "Done"),
                (Failed, "Failed"),
                )

    action = models.CharField(choices=Actions, max_length=25)
    status = models.IntegerField(choices=Statuses, default=0)
    created = models.DateTimeField(auto_now_add=True)

    # last updated on server
    last_modified = models.DateTimeField(auto_now=True)

    # last updated on Pi
    status_updated_time = models.DateTimeField(default=timezone.now)

