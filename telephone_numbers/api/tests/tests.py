from rest_framework import status
from rest_framework.test import APITestCase


class TelephoneNumberTests(APITestCase):

    def test_get_all_telephone_numbers(self):
        """
        Ensure we can get the telephone numbers
        """
        url = '/telephone_numbers/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
