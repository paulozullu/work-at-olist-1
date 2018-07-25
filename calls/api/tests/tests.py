from rest_framework import status
from rest_framework.test import APITestCase

from calls.models import PhoneCall

calls = [
    {
        'type': PhoneCall.CallTypes.start.value,
        'source': {
            'phone_number': '00123456789'
        },
        'destination': {
            'phone_number': '00123456780'
        },
        'timestamp': '2018-07-24T12:40:00Z',
        'call_id': 1000
    },
    {
        'type': PhoneCall.CallTypes.end.value,
        'timestamp': '2018-07-24T12:42:00Z',
        'call_id': 1000
    }
]


class PhoneCallTests(APITestCase):
    url = '/calls/'

    def test_get_all_phone_calls(self):
        """
        Ensure phone calls can be gotten
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_start_call_end_call(self):
        """
        Ensure a start call and an end call object can be created
        """
        for call in calls:
            response = self.client.post(self.url, call, format='json')
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED
            )

    def test_create_start_call_without_source(self):
        """
        Ensure a start call cannot be created without a source
        """
        params = {

            'type': PhoneCall.CallTypes.start.value,
            'destination': {
                'phone_number': '00123456780'
            },
            'timestamp': '2018-07-24T12:40:00Z',
            'call_id': 1000
        }
        response = self.client.post(self.url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_start_call_without_destination(self):
        """
        Ensure a start call cannot be created without a destination
        """
        params = {
            'origin': '00123456789',
            'type': PhoneCall.CallTypes.start.value,
            'timestamp': '2018-07-24T12:40:00Z',
            'call_id': 1000
        }
        response = self.client.post(self.url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_call_same_call_id_type(self):
        """
        Ensure a call with the same call_id and type cannot be created
        """
        call1 = calls[0]
        call2 = {
            'type': PhoneCall.CallTypes.start.value,
            'source': {
                'phone_number': '00123456789'
            },
            'destination': {
                'phone_number': '00123456780'
            },
            'timestamp': '2018-07-24T12:50:00Z',
            'call_id': call1['call_id']
        }

        response = self.client.post(self.url, call1, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        response = self.client.post(self.url, call2, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_create_call_same_timestamp(self):
        """
        Ensure a call from the same origin can't be created
        at the same time of another call for that origin
        """
        params = calls[:]
        param = {
            'type': PhoneCall.CallTypes.start.value,
            'source': {
                'phone_number': '00123456789'
            },
            'destination': {
                'phone_number': '00123456780'
            },
            'timestamp': '2018-07-24T12:40:00Z',
            'call_id': 1001
        }
        params.append(param)

        for call in params:
            response = self.client.post(self.url, call, format='json')
            if call == params[2]:
                self.assertEqual(
                    response.status_code, status.HTTP_400_BAD_REQUEST
                )
            else:
                self.assertEqual(
                    response.status_code, status.HTTP_201_CREATED
                )

    def test_create_call_within_timestamp(self):
        """
        Ensure a call from the same origin can't be created
        within the same time of another call for that origin
        """
        params = calls[:]
        param = {
            'type': PhoneCall.CallTypes.start.value,
            'source': {
                'phone_number': '00123456789'
            },
            'destination': {
                'phone_number': '00123456780'
            },
            'timestamp': '2018-07-24T12:41:00Z',
            'call_id': 1001
        }
        params.append(param)

        for call in params:
            response = self.client.post(self.url, call, format='json')
            if call == params[2]:
                self.assertEqual(
                    response.status_code, status.HTTP_400_BAD_REQUEST
                )
            else:
                self.assertEqual(
                    response.status_code, status.HTTP_201_CREATED
                )

    def test_create_end_call_without_start_call(self):
        """
        Ensure an end call cannot be created if a start
        call with the same call_id exists
        """
        params = calls[1]
        response = self.client.post(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BillTests(APITestCase):
    source = '00123456789'
    period = '07/2018'

    def test_get_all_bills(self):
        """
        Ensure we can get the bills
        """
        url = '/bills/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_bill_origin_period(self):
        """
        Ensure we can get the bills for an origin in a given period
        """
        url_calls = '/calls/'
        for call in calls:
            self.client.post(url_calls, call, format='json')

        url_bills = '/bills/get_period_bill/?origin={0}&period={1}' \
            .format(self.source, self.period)
        response = self.client.get(url_bills, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_get_bill_origin(self):
        """
        Ensure we can get the bills for an origin
        """
        url_bills = '/bills/get_period_bill/?origin={0}' \
            .format(self.source)
        response = self.client.get(url_bills, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
