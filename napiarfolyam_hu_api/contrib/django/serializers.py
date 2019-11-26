from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class CurrencyConverterSerializer(serializers.Serializer):
    from_amount = serializers.FloatField(
        label=_('from amount'),
        min_value=0,
        )
    from_currency = serializers.ChoiceField(
        label=_('from currency'),
        choices=settings.CURRENCY_CHOICES,
        required=True,
        )
    to_currency = serializers.ChoiceField(
        label=_('to currency'),
        choices=settings.CURRENCY_CHOICES,
        required=False,
        allow_blank=True,
        )
