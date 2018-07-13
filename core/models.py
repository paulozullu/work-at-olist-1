from datetime import timedelta

from django.db import models

from telephone_numbers.models import TelephoneNumber


class Bill(models.Model):
    """
    Bill model.
    """
    origin = models.ForeignKey(
        TelephoneNumber, related_name='source',
        on_delete=models.CASCADE)
    destination = models.ForeignKey(
        TelephoneNumber, related_name='destination',
        on_delete=models.CASCADE
    )
    call_id = models.IntegerField(unique=True, null=True)
    call_start_date = models.DateField()
    call_start_time = models.TimeField()
    call_duration = models.DurationField(default=timedelta(seconds=0))
    call_price = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )

    def __str__(self):
        return "Origin: {0} <> Destination: {1} <> Date: {2} <> Time: {3} <> Duration:" \
               " {4} <> Price: {5}".format(
            self.origin, self.destination, self.call_start_date, self.call_start_time,
            self.call_duration, self.call_price
        )

