from django.core.validators import RegexValidator
from django.db import models


class TelephoneNumber(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,11}$',
        message='Phone number must be entered in the format: "9999999999".'
                ' The first two digits are the area code.'
                ' The phone number is composed of 8 or 9 digits.'
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=11, null=True, default=None
    )

    def __str__(self):
        return self.phone_number
