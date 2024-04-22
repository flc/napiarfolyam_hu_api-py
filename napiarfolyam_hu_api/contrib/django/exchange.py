import itertools
import functools
import logging
from decimal import Decimal

from django.core.cache import cache
from django.conf import settings

from napiarfolyam_hu_api import get_mnb


logger = logging.getLogger(__name__)


def get_safe(func, cache_key, default):
    try:
        value = func()
    except Exception as e:
        logger.exception("Couldn't get the value from napiarfolyam.hu")
        # try to get it from cache
        value = cache.get(cache_key)
        if value is not None:
            return value
        logger.exception("Couldn't get the value from cache")
        # this is silly but we really need some data
        return default
    else:
        # cache forever
        cache.set(cache_key, value, timeout=None)
        return value


def get_mnb_safe(currency, cache_first=False, default=None):
    cache_key = "currency:mnb:{}".format(currency)
    if cache_first:
        value = cache.get(cache_key)
        if value:
            return value
    return get_safe(
        functools.partial(get_mnb, currency),
        cache_key, default
        )


def get_exchange_rate_data(cache_first=True):
    rates = {}
    for c in settings.CURRENCIES:
        c = c.lower()
        rates[c] = get_mnb_safe(currency=c, cache_first=cache_first)

    data = {}
    for c1, c2 in itertools.permutations(rates.keys(), 2):
        data[(c1.upper(), c2.upper())] = rates[c1] / rates[c2]
    return data


def get_exchange_rate(from_currency, to_currency, exchange_rate_data=None):
    if from_currency == to_currency:
        return 1.0

    assert(from_currency in settings.CURRENCIES), 'from currency is not supported'
    assert(to_currency in settings.CURRENCIES), 'to currency is not supported'

    data = exchange_rate_data or get_exchange_rate_data()

    return data[(from_currency, to_currency)]


def convert_currency(
    value, from_currency, to_currency, exchange_rate_data=None
    ):
    rate = get_exchange_rate(from_currency, to_currency, exchange_rate_data)
    if isinstance(value, Decimal):
        rate = Decimal(rate)
    return rate * value


def refresh_exchange_rates():
    return get_exchange_rate_data(cache_first=False)


def get_exchange_rate_data_for_date(date):
    rates = {}
    for c in settings.CURRENCIES:
        c = c.lower()
        rates[c] = get_mnb(currency=c, date=date)

    data = {}
    for c1, c2 in itertools.permutations(rates.keys(), 2):
        data[(c1.upper(), c2.upper())] = rates[c1] / rates[c2]
    return data
