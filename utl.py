from datetime import datetime, timedelta
import logging

from constants import CURRENCY, LIST_OF_CURRENCIES, URL_PB


def create_list_url(days: int) -> list[str]:
    today = datetime.today()
    urls = [URL_PB + (datetime.strftime(today - timedelta(days=day), '%d.%m.%Y')) for day in range(days)]
    return urls


def get_currencies(argv):
    currencies = list(CURRENCY)
    if len(argv) > 2:
        for el in argv[2:]:
            if el.upper() in LIST_OF_CURRENCIES:
                currencies.append(el.upper())
    return set(currencies)


def get_days_from_request(arg) -> int:
    try:
        days = int(arg[1]) if len(arg) > 1 else 1
    except ValueError:
        days = 1
        logging.info('Incorrect number of days. Results will be done for 1 day.')
    if days <= 0:
        days = 1
        logging.info('Incorrect number of days. Results will be done for 1 day.')
    if days > 10:
        days = 10
        logging.info('Incorrect number of days. Results will be done for 10 days.')
    return days


def selection_fields(response, currencies=('EUR', 'USD')) -> dict:
    if 'exchangeRate' in response:
        total_rates = response['exchangeRate']
        rates = {rate.get("currency"): {'sale': rate.get('saleRate', rate.get('saleRateNB')),
                                        'purchase': rate.get('purchaseRate', rate.get('purchaseRateNB'))}
                 for rate in total_rates if rate.get("currency", '') in currencies
                 }
    else:
        rates = response
    return rates
