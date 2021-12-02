import asyncio
import websockets

class WSUtil:
    clients = set()

    async def handler(self, websocket):
        self.clients.add(websocket)

        try:
            async for message in websocket:
                print(message)
                await websocket.send(message)
        finally:
            self.clients.remove(websocket)

    async def main(self):
        async with websockets.serve(self.handler, "localhost", 8765):
            await asyncio.Future() 

    def run(self):
        asyncio.run(self.main())

    def broadcast(self, message):
        websockets.broadcast(self.clients, message)

WS = WSUtil()