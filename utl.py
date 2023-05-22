from datetime import datetime, timedelta

LIST_OF_CURRENCIES = {
    'USD',
    'EUR',
    'CHF',
    'GBP',
    'PLZ',
    'SEK',
    'XAU',
    'CAD'
}


def create_set_url(days: int) -> set:
    url_pb = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
    curr_d = datetime.today()
#    list_url = []
    url_set = {url_pb + (datetime.strftime(curr_d - timedelta(days=day), '%d.%m.%Y')) for day in range(days)}
    print(url_set)
    return url_set


def get_days_from_request(arg) -> int:
    try:
        days = int(arg[1]) if len(arg) > 1 else 1
    except ValueError:
        days = 1
        print('Incorrect number of days. Results will be done for 1 day.')
    if days <= 0:
        days = 1
        print('Incorrect number of days. Results will be done for 1 day.')
    if days > 10:
        days = 10
        print('Incorrect number of days. Results will be done for 10 day.')
    return days


def get_currencies(argv):
    currencies = ['EUR', 'USD']
    if len(argv) > 2:
        print(argv[2:])
        currencies_n = [currencies.append(el.upper()) for el in argv[2:] if el.upper() in LIST_OF_CURRENCIES]
    print(f'rate {currencies_n}')
    return set(currencies)


if __name__ == "__main__":
   exit(create_set_url(4))