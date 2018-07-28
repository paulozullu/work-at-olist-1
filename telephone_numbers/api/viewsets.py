from rest_framework.viewsets import ModelViewSet

from telephone_numbers.api.serializers import TelephoneNumberSerializer
from telephone_numbers.models import TelephoneNumber


class TelephoneNumberViewSet(ModelViewSet):
    """
    retrieve:
        Return a telephone number instance.

    list:
        Return all telephone numbers.
    """
    queryset = TelephoneNumber.objects.all()
    serializer_class = TelephoneNumberSerializer
    http_method_names = ['get']
