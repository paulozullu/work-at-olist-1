from datetime import timedelta, time
from enum import Enum

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from telephone_numbers.models import TelephoneNumber

STANDARD_PRICE_RULES = {'start': '6:00', 'finish': '22:00', 'standing_charge': 0.36, 'call_charge': 0.09}
REDUCED_PRICE_RULES = {'start': '22:00', 'finish': '06:00', 'standing_charge': 0.36, 'call_charge': 0.00}


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class PhoneCall(models.Model):
    """
    Phone call model.
    """

    class CallTypes(ChoiceEnum):
        start = 'start'
        end = 'end'

    type = models.CharField(max_length=5, choices=CallTypes.choices())
    timestamp = models.DateTimeField()
    call_id = models.IntegerField()
    source = models.ForeignKey(
        TelephoneNumber, related_name='source_number',
        on_delete=models.PROTECT, null=True, blank=True
    )
    destination = models.ForeignKey(
        TelephoneNumber, related_name='destination_number',
        on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        """
        Certificate that each call has only one record of each type.
        """
        unique_together = ('type', 'call_id')

    def __str__(self):
        return "%d - %s" % (self.call_id, self.type)


@receiver(post_save, sender=PhoneCall, dispatch_uid="create_bill")
def create_bill(sender, instance, **kwargs):
    """
    Create the related Bill after finishing and saving the call.
    """
    if instance.type == PhoneCall.CallTypes.end.value:

        if not Bill.objects.filter(call_id=instance.call_id).exists():
            start_call = PhoneCall.objects.get(
                type=PhoneCall.CallTypes.start.value, call_id=instance.call_id
            )

            bill = Bill()
            bill.origin = start_call.source
            bill.destination = start_call.destination
            bill.call_id = instance.call_id
            bill.call_start_date = start_call.timestamp.date()
            bill.call_start_time = start_call.timestamp.time()
            bill.call_duration = bill.get_duration(
                instance.timestamp, start_call.timestamp
            )
            bill.price = bill.get_price(
                instance.timestamp, start_call.timestamp
            )
            bill.save()


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
        return "Origin: {0} <> Destination: {1} <> Date: {2} <> " \
               "Time: {3} <> Duration: {4} <> Price: {5}".format(
                self.origin, self.destination, self.call_start_date,
                self.call_start_time, self.call_duration, self.call_price
                )

    @staticmethod
    def get_duration(end_date, start_date):
        """
        Get the call duration.

            Args:
                end_date (DateTime): Call end date.
                start_date (DateTime): Call start date.

            Return:
                timedelta: Call duration.
        """
        return end_date - start_date

    @staticmethod
    def get_price(end, start):
        """
        Get the call price.

            Return:
                decimal: Call price.
        """
        standard_minutes = 0

        while start < end:
            start = start + timedelta(minutes=1)

            if start < end and time(6, 0, 0) < start.time() <= time(22, 0, 0):
                standard_minutes += 1

        price = STANDARD_PRICE_RULES['standing_charge'] + \
                (standard_minutes * STANDARD_PRICE_RULES['call_charge'])

        return price
