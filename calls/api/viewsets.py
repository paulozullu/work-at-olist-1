from datetime import datetime, date

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from calls.api.serializers import PhoneCallSerializer, BillSerializer
from calls.models import PhoneCall, Bill
from calls.utils import get_previous_month


class PhoneCallViewSet(ModelViewSet):
    """
    retrieve:
        Return a phone call instance.

    list:
        Return all phone calls, ordered by call_id and type.

    create:
        Create a new phone call.
        Start calls must have source and destination numbers.

    delete:
        Remove an existing phone call.

    partial_update:
        Update one or more fields on an existing phone call.
        Start calls must have source and destination numbers.

    update:
        Update a phone call.
        Start calls must have source and destination numbers.
    """
    queryset = PhoneCall.objects.order_by('call_id', '-type')
    serializer_class = PhoneCallSerializer


class BillViewSet(ModelViewSet):
    """
    retrieve:
        Return a bill instance.

    list:
        Return all bills.
    """
    queryset = Bill.objects.order_by('call_id', 'call_start_date')
    serializer_class = BillSerializer
    http_method_names = ['get']
    origin = openapi.Parameter(
        'origin',
        openapi.IN_QUERY,
        description="Phone number that originated the bill calls.",
        type=openapi.TYPE_STRING,
        required=True
    )
    period = openapi.Parameter(
        'period',
        openapi.IN_QUERY,
        description="Reference period (month/year). If the reference"
                    " period is not informed the system will consider"
                    " the last month.",
        type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(method='get', manual_parameters=[origin, period])
    @action(methods=['get'], detail=False)
    def get_period_bill(self, request):
        """
        Get the telephone bill of a given origin number for a month. 
        If the period is not passed must get the bill of the last month.
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

        bills = bills.filter(
            call_end_date__month=month,
            call_end_date__year=year
        ).order_by('call_start_time')

        ctx = {'request': request}
        serializer = BillSerializer(bills, context=ctx, many=True)

        return Response(serializer.data)
