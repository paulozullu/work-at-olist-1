from rest_framework.viewsets import ModelViewSet

from telephone_numbers.api.serializers import TelephoneNumberSerializer
from telephone_numbers.models import TelephoneNumber


class TelephoneNumberViewSet(ModelViewSet):
    """
    ViewSet for TelephoneNumber
    """
    queryset = TelephoneNumber.objects.all()
    serializer_class = TelephoneNumberSerializer
    http_method_names = ['get']
