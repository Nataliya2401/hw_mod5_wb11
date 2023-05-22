import asyncio
from datetime import datetime, timedelta
import json
import logging
import platform
import sys

import aiohttp

CURRENCY = ('EUR', 'USD')
LIST_OF_CURRENCIES = {
    'USD',
    'EUR',
    'CHF',
    'GBP',
    'PLN',
    'SEK',
    'XAU',
    'CAD',



}

URL_PB = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
logging.basicConfig(level=logging.INFO)


def create_list_url(days: int) -> list[str]:
    curr_d = datetime.today()
    urls = [URL_PB + (datetime.strftime(curr_d - timedelta(days=day), '%d.%m.%Y')) for day in range(days)]
    return urls


def get_currencies(argv):
    currencies = ['EUR', 'USD']
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


def selection_fields(response, currencies=('EUR', 'USD')):
    total_rates = response['exchangeRate']
    rates = {rate.get("currency"): {'sale': rate.get('saleRate', 'saleRateNB'),
                                    'purchase': rate.get('purchaseRate', 'purchaseRateNB')}
             for rate in total_rates if rate.get("currency", '') in currencies
             }
    return rates


async def request(url, currencies):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    result = {r['date']: selection_fields(r, currencies)}
                    return result
                logging.error(f'Error status {resp.status} for {url}')
        except aiohttp.ClientConnectionError as e:
            logging.error(f'Connection Error for {url}: {e}')
        return None


async def get_exchange(urls, currencies):
    list_requests = [request(url, currencies) for url in urls]
    res = await asyncio.gather(*list_requests, return_exceptions=True)
    return res


def main():
    argv = sys.argv
    days = get_days_from_request(argv)
    currencies = get_currencies(argv)
    urls = create_list_url(days)
    r = asyncio.run(get_exchange(urls, currencies))
    print(json.dumps(r, indent=2))


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    exit(main())
