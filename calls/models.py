from django.db import models

from telephone_numbers.models import TelephoneNumber

CALL_TYPES = [
    ("start", "start"),
    ("end", "end"),
]


class PhoneCall(models.Model):
    """
    Phone call model.
    """
    type = models.CharField(max_length=5, choices=CALL_TYPES)
    timestamp = models.DateTimeField()
    call_id = models.IntegerField()
    source = models.ForeignKey(
        TelephoneNumber, related_name='source_number',
        on_delete=models.PROTECT, null=True, default=None
    )
    destination = models.ForeignKey(
        TelephoneNumber, related_name='destination_number',
        on_delete=models.PROTECT, null=True, default=None
    )

    class Meta:
        """
        Certificate that each call has only one record of each type.
        """
        unique_together = ('type', 'call_id')

    def __str__(self):
        return "%d - %s" % (self.call_id, self.type)
