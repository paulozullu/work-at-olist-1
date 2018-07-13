from datetime import timedelta, time

from django.db import models

from telephone_numbers.models import TelephoneNumber

STANDARD_PRICE_RULES = {'start': '6:00', 'finish': '22:00', 'standing_charge': 0.36, 'call_charge': 0.09}
REDUCED_PRICE_RULES = {'start': '22:00', 'finish': '06:00', 'standing_charge': 0.36, 'call_charge': 0.00}


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
            
        price = STANDARD_PRICE_RULES['standing_charge'] + (standard_minutes * STANDARD_PRICE_RULES['call_charge']) 
        
        return price
