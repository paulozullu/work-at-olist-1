from rest_framework.viewsets import ModelViewSet

from calls.api.serializers import PhoneCallSerializer
from calls.models import PhoneCall


class PhoneCallViewSet(ModelViewSet):
    """
    ViewSet for phone call.
    """
    queryset = PhoneCall.objects.order_by('call_id', '-type')
    serializer_class = PhoneCallSerializer
    http_method_names = ['get']
