from datetime import datetime, date

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from calls.api.serializers import PhoneCallSerializer, BillSerializer
from calls.models import PhoneCall, Bill
from calls.utils import get_previous_month


class PhoneCallViewSet(ModelViewSet):
    """
    ViewSet for phone call.
    """
    queryset = PhoneCall.objects.order_by('call_id', '-type')
    serializer_class = PhoneCallSerializer


class BillViewSet(ModelViewSet):
    """
    ViewSet for Bill.
    """
    queryset = Bill.objects.order_by('call_id', 'call_start_date')
    serializer_class = BillSerializer

    @action(methods=['get'], detail=False)
    def get_period_bill(self, request):
        """
        Get the telephone bill for a month. If the is not period passed,
        must get the bill fot last month.


        Return:
            json: List of calls and bills for a month.
        """
        origin = request.query_params['origin']
        period = request.query_params.get('period', None)
        bills = Bill.objects.filter(origin__phone_number=origin)

        if period is not None:

            try:

                period = datetime.strptime(period, '%m/%Y')
                month = period.month
                year = period.year
            except ValueError:

                message = 'The period must be in month/year format!'
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

        else:

            month, year = get_previous_month(date.today())

        bills = bills.filter(call_end_date__month=month, call_end_date__year=year)

        ctx = {'request': request}
        serializer = BillSerializer(bills, context=ctx, many=True)

        return Response(serializer.data)
