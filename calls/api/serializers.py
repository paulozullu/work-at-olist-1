from rest_framework.serializers import ModelSerializer

from calls.models import PhoneCall
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
