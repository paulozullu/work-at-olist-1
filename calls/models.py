from django.core.validators import RegexValidator
from django.db import models

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
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,11}$',
        message='Phone number must be entered in the format: "9999999999".'
                ' The first two digits are the area code.'
                ' The phone number is composed of 8 or 9 digits.'
    )
    source = models.CharField(
        validators=[phone_regex], max_length=11, null=True, default=None
    )
    destination = models.CharField(
        validators=[phone_regex], max_length=11, null=True, default=None
    )

    def __str__(self):
        return "%d - %s" % (self.call_id, self.type)
