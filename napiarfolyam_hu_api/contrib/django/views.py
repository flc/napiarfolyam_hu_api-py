import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from .exchange import *
from .serializers import CurrencyConverterSerializer


logger = logging.getLogger(__name__)


class CurrencyConverterView(APIView):

    def get(self, request, format=None, **kwargs):
        ser = CurrencyConverterSerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)
        data = ser.data

        from_amount = data['from_amount']
        from_currency = data['from_currency']
        to_currency = data.get('to_currency', None)

        currencies = settings.CURRENCIES

        if to_currency:
            currencies = [to_currency]
        else:
            try:
                currencies.remove(from_currency)
            except ValueError:
                raise

        exchange_rate_data = get_exchange_rate_data()

        convs = []
        for to_currency in currencies:
            to_amount = convert_currency(
                value=from_amount,
                from_currency=from_currency,
                to_currency=to_currency,
                exchange_rate_data=exchange_rate_data,
                )
            convs.append({
                'from_amount': from_amount,
                'from_currency': from_currency,
                'to_amount': to_amount,
                'to_currency': to_currency,
            })

        exchange_rates = [
            {'from_currency': k[0], 'to_currency': k[1], 'value': v}
            for k, v in exchange_rate_data.items()
            ]

        return Response({
            'conversions': convs,
            'exchange_rates': exchange_rates,
            })
