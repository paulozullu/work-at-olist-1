from enum import Enum

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Bill
from telephone_numbers.models import TelephoneNumber


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
