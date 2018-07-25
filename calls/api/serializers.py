from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer

from calls.models import PhoneCall, Bill
from telephone_numbers.api.serializers import TelephoneNumberSerializer
from telephone_numbers.models import TelephoneNumber


class PhoneCallSerializer(ModelSerializer):
    """
    Serializer for phone call.
    """

    source = TelephoneNumberSerializer(many=False, required=False)
    destination = TelephoneNumberSerializer(many=False, required=False)

    class Meta:
        model = PhoneCall
        fields = (
            'type', 'source', 'destination', 'timestamp', 'call_id'
        )

    def create(self, validated_data):
        """
        Overrides ModelSerializer create method.
            Args:
                validated_data (dict): The data after validation.

            Returns:
                PhoneCall object created.
        """
        if validated_data['type'] == PhoneCall.CallTypes.start.value:
            source_data = validated_data['source']
            del validated_data['source']
            source, created = TelephoneNumber.objects.get_or_create(
                phone_number=source_data['phone_number']
            )

            destination_data = validated_data['destination']
            del validated_data['destination']
            destination, created = TelephoneNumber.objects.get_or_create(
                phone_number=destination_data['phone_number']
            )

        try:
            call = PhoneCall.objects.create(**validated_data)
        except IntegrityError:
            message = 'A call with the same type and call_id already exists!'
            raise APIException(message)

        if validated_data['type'] == PhoneCall.CallTypes.start.value:
            call.source = source
            call.destination = destination
            call.save()

        return call

    def validate(self, data):
        """
        Check if the data is valid.

            Args:
                 data (dict): The data to be validated.

            Returns:
                Dict containing the validated data.
        """
        if data['type'] == PhoneCall.CallTypes.end.value:

            try:
                start_call = PhoneCall.objects.get(
                    call_id=data['call_id'],
                    type=PhoneCall.CallTypes.start.value
                )

                source = start_call.source

                if start_call.timestamp > data['timestamp']:  # Check if end
                    # call time is bigger than start call
                    message = 'End call time must be greater than ' \
                              'start call time.'
                    raise serializers.ValidationError(message)

            except ObjectDoesNotExist:  # Error if start call does not exist
                #  for a new end call
                message = 'You can\'t add an end call without a start call.'
                raise serializers.ValidationError(message)

        elif data['type'] == PhoneCall.CallTypes.start.value:
            try:
                source = data['source']['phone_number']
                destination = data['destination']['phone_number']
            except KeyError:
                message = 'Source number and destination number must ' \
                          'exist for start calls'
                raise serializers.ValidationError(message)

            if source == '' or destination == '':
                message = 'Source number and destination number cannot ' \
                          'be blank'
                raise serializers.ValidationError(message)

        call_ids = Bill.objects.filter(
            Q(call_start_date=data['timestamp'].date())
            | Q(call_end_date=data['timestamp'].date()),
            origin__phone_number=source
        ).values_list('call_id', flat=True).distinct()

        for call_id in call_ids:
            # Check if another call for that source within the time exists
            start_time = PhoneCall.objects.filter(
                call_id=call_id, type=PhoneCall.CallTypes.start.value
            ).values('timestamp')[0]

            try:
                end_time = PhoneCall.objects.filter(
                    call_id=call_id, type=PhoneCall.CallTypes.end.value
                ).values('timestamp')[0]
            except IndexError:
                end_time = None

            if start_time and end_time:

                if start_time['timestamp'] <= \
                        data['timestamp'] <= end_time['timestamp']:
                    message = 'There\'s already another call in this time.'
                    raise serializers.ValidationError(message)

        return data


class BillSerializer(ModelSerializer):
    """
    Serializer for Bill.
    """

    destination = TelephoneNumberSerializer(many=False)

    class Meta:
        model = Bill
        fields = (
            'destination', 'call_start_date',
            'call_start_time', 'call_duration', 'call_price'
        )
