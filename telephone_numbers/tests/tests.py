from django.test import TestCase

from telephone_numbers.models import TelephoneNumber as TelephoneNumberModel


class TelephoneNumberTestCase(TestCase):
    """
    Test module for TelephoneNumber model
    """

    def setUp(self):
        TelephoneNumberModel.objects.create(
            phone_number='123456789'
        )
        TelephoneNumberModel.objects.create(
            phone_number='123456780'
        )

    def test_created(self):
        """
        Test whether telephone numbers are created
        """

        number_123456789 = TelephoneNumberModel.objects.get(phone_number='123456789')
        number_123456780 = TelephoneNumberModel.objects.get(phone_number='123456780')
        self.assertIsNotNone(number_123456789)
        self.assertIsNotNone(number_123456780)
