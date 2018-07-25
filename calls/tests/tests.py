from datetime import datetime, timezone

from django.test import TestCase

from calls.models import PhoneCall, Bill
from telephone_numbers.models import TelephoneNumber


class PhoneCallTestCase(TestCase):
    """
    Test module for Call model
    """

    def setUp(self):
        source = TelephoneNumber.objects.create(
            phone_number='123456789'
        )
        destination = TelephoneNumber.objects.create(
            phone_number='123456780'
        )

        PhoneCall.objects.create(
            type=PhoneCall.CallTypes.start.value,
            source=source,
            destination=destination,
            timestamp=datetime.now(timezone.utc),
            call_id=12345
        )

        PhoneCall.objects.create(
            type=PhoneCall.CallTypes.end.value,
            timestamp=datetime.now(timezone.utc),
            call_id=12345
        )

    def test_created_phone_call_bill(self):
        """
        Test whether the PhoneCalls and the Bill were created
        """
        start_call = PhoneCall.objects.get(
            type=PhoneCall.CallTypes.start.value,
            call_id=12345
        )
        end_call = PhoneCall.objects.get(
            type=PhoneCall.CallTypes.end.value,
            call_id=12345
        )
        bill = Bill.objects.get(call_id=12345)

        self.assertIsNotNone(start_call)
        self.assertIsNotNone(end_call)
        self.assertIsNotNone(bill)
