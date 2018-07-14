from rest_framework.viewsets import ModelViewSet

from calls.api.serializers import PhoneCallSerializer, BillSerializer
from calls.models import PhoneCall, Bill


class PhoneCallViewSet(ModelViewSet):
    """
    ViewSet for phone call.
    """
    queryset = PhoneCall.objects.order_by('call_id', '-type')
    serializer_class = PhoneCallSerializer
    http_method_names = ['get']


class BillViewSet(ModelViewSet):
    """
    ViewSet for Bill.
    """
    queryset = Bill.objects.order_by('call_id', 'call_start_date')
    serializer_class = BillSerializer
    http_method_names = ['get']
