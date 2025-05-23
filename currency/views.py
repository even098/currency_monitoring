from django.utils.timezone import now

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from .models import User, Currency

from currency_monitoring.settings import API_KEY, BASE_URL

from .models import Subscription
from .serializers import CurrencySerializer


class RegisterUserAPIView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data.get('telegram_id')
            notify_time = request.data.get('notify_time')
            user = User.objects.get_or_create(telegram_id=telegram_id, notify_time=notify_time)

            return Response(
                data={
                    'detail': 'Registered successfully!',
                    'telegram_id': telegram_id,
                    'notify_time': notify_time
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CurrenciesAPIView(APIView):
    def get(self, request):
        response = requests.get(f'{BASE_URL}/{API_KEY}/codes')
        data = response.json()
        supported_codes = data.get('supported_codes')

        if supported_codes:
            return Response(data={'supported_codes': data['supported_codes']}, status=status.HTTP_200_OK)

        return Response(data={'detail': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubscribeToCurrencyAPIView(APIView):
    def post(self, request):
        data = request.data
        telegram_id = data.get('telegram_id')
        user = get_object_or_404(User, telegram_id=telegram_id)
        base_currency_code = data.get('base_currency_code')
        target_currency_code = data.get('target_currency_code')

        try:
            currency = Currency.objects.get(
                base_currency_code=base_currency_code,
                target_currency_code=target_currency_code
            )
        except Currency.DoesNotExist:
            url = f'{BASE_URL}/{API_KEY}/latest/{base_currency_code}'
            response = requests.get(url)
            currency_data = response.json()
            rate = currency_data.get('conversion_rates').get(target_currency_code)

            currency = Currency.objects.create(
                base_currency_code=base_currency_code,
                target_currency_code=target_currency_code,
                rate=rate
            )

        subscription, created = Subscription.objects.get_or_create(
            user=user,
            currency=currency,
        )

        if created:
            return Response(data={'detail': 'Subscription created!'}, status=status.HTTP_201_CREATED)

        return Response(data={'detail': 'Subscription already exists.'}, status=status.HTTP_409_CONFLICT)


class SubscriptionsAPIView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        user = get_object_or_404(User, telegram_id=telegram_id)
        subscriptions = user.subscriptions.all()
        currencies = Currency.objects.filter(subscriptions__in=subscriptions)
        serialized_currencies_data = CurrencySerializer(currencies, many=True).data

        return Response(data={'subscriptions': serialized_currencies_data}, status=status.HTTP_200_OK)


class CurrencyRatesUpdateAPIView(APIView):
    def get(self, request):
        try:
            base_currency_codes = Currency.objects.values_list('base_currency_code', flat=True)
            target_currency_codes = Currency.objects.values_list('target_currency_code', flat=True)

            for base_currency_code in base_currency_codes:
                currency_data = requests.get(f'{BASE_URL}/{API_KEY}/latest/{base_currency_code}').json()
                conversion_rates = currency_data.get('conversion_rates')

                for target_currency_code in target_currency_codes:
                    rate = conversion_rates.get(target_currency_code)

                    Currency.objects.filter(
                        base_currency_code=base_currency_code,
                        target_currency_code=target_currency_code
                    ).update(
                        rate=rate,
                        last_updated=now()
                    )

            return Response(data={'detail': 'All currencies updated successfully!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                data={'detail': 'An error occured', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangeNotificationTimeAPIView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data.get('telegram_id')
            notify_time = request.data.get('notify_time')

            user = User.objects.filter(telegram_id=telegram_id).update(notify_time=notify_time)

            return Response(
                data={
                    'detail': 'Updated successfully!',
                    'telegram_id': telegram_id,
                    'notify_time': notify_time
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteSubscriptionAPIView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        base_currency_code = request.data.get('base_currency_code')
        target_currency_code = request.data.get('target_currency_code')
        print(telegram_id, base_currency_code, target_currency_code)
        user = get_object_or_404(User, telegram_id=telegram_id)
        currency = get_object_or_404(Currency, base_currency_code=base_currency_code, target_currency_code=target_currency_code)
        subscription = get_object_or_404(Subscription, user=user, currency=currency)
        subscription.delete()

        return Response(data={'detail': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
