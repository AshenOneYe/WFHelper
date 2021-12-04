import asyncio
import websockets
from multiprocessing import Process


class WS(Process):
    clients = set()
    conn = None

    def onMessage(self, data):
        self.broadcast(data)

    async def handler(self, websocket):
        self.clients.add(websocket)

        try:
            async for message in websocket:
                await websocket.send(message)
        finally:
            self.clients.remove(websocket)

    async def main(self):
        async with websockets.serve(self.handler, "localhost", 8765):
            await asyncio.Future()

    def run(self):
        self.conn.setCallback(self.onMessage)
        self.conn.startReceive()
        asyncio.run(self.main())

    def broadcast(self, message):
        websockets.broadcast(self.clients, message)

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
