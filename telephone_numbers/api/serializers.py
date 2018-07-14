from rest_framework.serializers import ModelSerializer

from telephone_numbers.models import TelephoneNumber


class TelephoneNumberSerializer(ModelSerializer):
    """
    Serializer for telephone.
    """

    class Meta:
        model = TelephoneNumber
        fields = '__all__'
