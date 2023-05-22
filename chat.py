import asyncio
import logging

import aiohttp
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from constants import CURRENCY
from utl import create_list_url, selection_fields
from main import get_exchange

logging.basicConfig(level=logging.INFO)


async def get_exchange(days: int) -> str:
    urls = create_list_url(days)
    list_requests = [request(url) for url in urls]
    res = await asyncio.gather(*list_requests, return_exceptions=True)
    print(res)
    return str(res)


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return {r['date']: selection_fields(r, CURRENCY)}
                logging.error(f'Error status {resp.status} for {url}')
        except aiohttp.ClientConnectionError as e:
            logging.error(f'Connection Error for {url}: {e}')
        return None


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if 'exchange' in message:
                try:
                    day_message = int(message.split()[1])
                except ValueError:
                    day_message = 1
                print(day_message)
                message = await get_exchange(day_message)
                await self.send_to_clients(message)
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())

