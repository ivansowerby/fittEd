from data.enum import Data
from websockets.asyncio.client import connect
from json import dumps as json_dumps, loads as json_loads
import asyncio
from termcolor import colored

async def subscribe(callback):
    def parse_block(message: str) -> dict:
        return json_loads(message).get('x', {})

    def make_operation(opcode: str) -> dict:
        return json_dumps({'op': opcode})
    
    def get_operation(message: str) -> str:
        return json_loads(message).get('op', '')

    API_URL = Data.BitcoinEnum.API_URL.value
    async with connect(API_URL) as websocket:
        await websocket.send(
            make_operation('ping_block')
        )
        first_block = parse_block(await websocket.recv())
        callback(first_block)
        
        await websocket.send(
            make_operation('blocks_sub')
        )
        async def keep_alive():
            elapsed = 0
            while True:
                await websocket.send(
                    make_operation('ping')
                )
                await asyncio.sleep(20)
                elapsed += 20
                print(colored(f'...time elapsed: {elapsed}s', 'grey'))
        asyncio.create_task(keep_alive())

        while True:
            message = await websocket.recv()
            opcode = get_operation(message)
            if opcode == 'block':
                block = parse_block(message)
                callback(block)
            elif opcode == 'pong':
                continue
