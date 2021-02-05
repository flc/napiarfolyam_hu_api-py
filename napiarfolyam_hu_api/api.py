try:
    import urllib2 as urllib
except ImportError:
    import urllib
import datetime
import logging
from xml.dom import minidom

import requests

from .constants import BASE_URL, BANK_PARAM_VALUES, CURRENCY_PARAM_VALUES
from .utils import convert_date, parse_item_element
from .exceptions import InvalidParameterError, ParseError


def get_data(bank=None, currency=None, date=None, date_end=None, timeout=3):
    if bank is None and currency is None:
        raise InvalidParameterError("You have to specify either the 'bank' or "
                                    "'currency' parameter.")

    if bank is not None:
        bank_lower = bank.lower()
        if bank_lower not in BANK_PARAM_VALUES:
            raise InvalidParameterError(
                "The 'bank' parameter has to one of the following values: "
                "{}. You passed the value '{}'".format(
                                                    BANK_PARAM_VALUES, bank))
        bank = bank_lower

    if currency is not None:
        currency_upper = currency.upper()
        if currency_upper not in CURRENCY_PARAM_VALUES:
            raise InvalidParameterError(
                "The 'currency' parameter has to one of the following values: "
                "{}. You passed the value '{}'".format(
                                            CURRENCY_PARAM_VALUES, currency))
        currency = currency_upper

    if date is not None and date_end is not None:
        if (date_end - date).days > 31:
            raise InvalidParameterError("The time delta between the dates "
                                        "are maximum 31 days.")

    payload = {
        'bank': bank,
        'valuta': currency,
    }
    if date is not None:
        payload['datum'] = convert_date(date)
    if date_end is not None:
        payload['datumend'] = convert_date(date_end)

    response = requests.get(BASE_URL, params=payload, timeout=timeout)
    response_content = response.content

    try:
        document = minidom.parseString(response_content)
    except Exception as e:
        raise ParseError("Couldn't parse the response. "
                        "The response was: {}".format(response_content))

    item_elements = document.getElementsByTagName("item")
    return [parse_item_element(item_element)
            for item_element in item_elements]


get = get_data


def get_mnb(currency, date=None):
    if currency.lower() == 'huf':
        return 1.0
    data = get_data(bank="mnb", currency=currency, date=date)
    return float(data[0]['kozep'])
