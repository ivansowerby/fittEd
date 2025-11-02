import asyncio
import json
from asyncio import timeout_at

from websockets.asyncio.client import connect


async def init_socket(hook):
    async with connect("wss://ws.blockchain.info/inv") as websocket:
        await websocket.send(json.dumps({"op": "ping_block"}))
        message = await websocket.recv()

        print("test block: ", message)
        example_hook(json.loads(message)["x"])

        print("sending message to subscribe")
        await websocket.send(json.dumps({"op": "blocks_sub"}))

        async def ping():
            time = 0
            while True:
                print("it's been " + str(time) + " seconds")
                await websocket.send(json.dumps({"op": "ping"}))
                await asyncio.sleep(10)
                time += 10

        asyncio.create_task(ping())

        while True:
            message = await websocket.recv()

            print(message)

            message = json.loads(message)

            if message["op"] == "block":
                print("received block: ", message)
                hook(message["x"])
            elif message["op"] == "pong":
                print("ping received")


def example_hook(x):
    print("received block: ", x)

# this to run it with a hook that takes in the received block
def run(hook):
    asyncio.run(init_socket(hook))

if __name__ == "__main__":
    asyncio.run(init_socket(example_hook))