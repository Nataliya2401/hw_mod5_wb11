import asyncio
import json
import logging
import platform
import sys

import aiohttp

from utl import create_list_url, get_currencies, get_days_from_request, selection_fields


logging.basicConfig(level=logging.INFO)


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
