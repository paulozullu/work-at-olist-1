from rest_framework.serializers import ModelSerializer

from calls.models import PhoneCall, Bill
from telephone_numbers.api.serializers import TelephoneNumberSerializer


class PhoneCallSerializer(ModelSerializer):
    """
    Serializer for phone call.
    """

    source = TelephoneNumberSerializer(many=False)
    destination = TelephoneNumberSerializer(many=False)

    class Meta:
        model = PhoneCall
        fields = (
            'type', 'source', 'destination', 'timestamp', 'call_id'
        )


class BillSerializer(ModelSerializer):
    """
    Serializer for Bill.
    """

    origin = TelephoneNumberSerializer(many=False)
    destination = TelephoneNumberSerializer(many=False)

    class Meta:
        model = Bill
        fields = (
            'origin', 'destination', 'call_id', 'call_start_date',
            'call_start_time', 'call_duration', 'call_price'
        )
