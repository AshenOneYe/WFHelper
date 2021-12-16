import asyncio
import http
import json
import logging
import websockets
from os.path import splitext
from pathlib import Path
from utils import Log
from typing import Set, Any

logging.getLogger("websockets").setLevel(logging.ERROR)

CONTENT_TYPES = {
    ".css": "text/css",
    ".html": "text/html; charset=utf-8",
    ".ico": "image/x-icon",
    ".js": "text/javascript",
}


# TODO isDebug和instances应作为单独的信息传递给UI
class Server():
    isDebug = False

    instances = set()  # type: Set[Any]

    clients = set()  # type: Set[Any]
    streamClients = set()  # type: Set[Any]

    def __init__(self, instance=None, isDebug=False):
        if isDebug:
            Log.setDebugLevel()

            self.isDebug = isDebug

        if instance is not None:
            self.createInstance(instance)

    def createInstance(self, instance):
        instance.start()
        instance.setState({
            "key": "isDebug",
            "value": self.isDebug
        })
        instance.setEventHandler(self.eventHandler)

        self.instances.add(instance)

    def eventHandler(self, event):
        type = event["type"]

        # TODO 也应发送给对应实例
        if type == "onLogAppend" or type == "onStateUpdate":
            self.broadcast(
                self.clients,
                json.dumps({
                    "type": type,
                    "data": event["data"]
                }).encode('utf8')
            )
        elif type == "onFrameUpdate":
            self.broadcast(
                self.streamClients,
                event["data"]
            )

    async def handler(self, websocket, path):
        if path == "/websocket":
            await self.clientHandler(websocket)
        if path == "/stream":
            await self.streamHandler(websocket)

    async def clientHandler(self, websocket):
        async def send(queue, websocket):
            while True:
                try:
                    message = await queue.get()
                    await websocket.send(message)
                except Exception:
                    break

        queue = asyncio.Queue()

        task = asyncio.create_task(
            send(queue, websocket)
        )

        self.clients.add(queue)

        try:
            async for message in websocket:
                message = json.loads(message)

                # TODO 现在强制使用单例模式，应读取websocket对应实例
                for i in self.instances:
                    instance = i
                    break

                if "data" in message:
                    result = getattr(instance, message["type"])(message["data"])
                else:
                    result = getattr(instance, message["type"])()

                if result is not None:
                    await websocket.send(
                        json.dumps({
                            "type": message["type"] + "_ACK",
                            "data": result
                        }).encode('utf8')
                    )
        except Exception:
            pass
        finally:
            self.clients.remove(queue)

            task.cancel()

    async def streamHandler(self, websocket):
        async def send(queue, websocket):
            while True:
                try:
                    message = await queue.get()
                    await websocket.send(message)
                except Exception:
                    break

        queue = asyncio.Queue(1)

        task = asyncio.create_task(
            send(queue, websocket)
        )

        self.streamClients.add(queue)

        try:
            await websocket.wait_closed()
        except Exception:
            pass
        finally:
            self.streamClients.remove(queue)

            task.cancel()

    async def requestHandler(self, path, request_headers):
        if path == "/websocket":
            return
        if path == "/stream":
            return

        name, ext = splitext(path)

        if name[-1] == '/':
            name = name[1:] + "index"
        else:
            name = name[1:]

        if len(ext) == 0:
            ext = ".html"

        source = Path(__file__).parent.joinpath(name + ext)

        if source.is_file() and source.suffix in CONTENT_TYPES:
            headers = {
                "Content-Type": CONTENT_TYPES[source.suffix]
            }

            body = source.read_bytes()

            return http.HTTPStatus.OK, headers, body

        return http.HTTPStatus.NOT_FOUND, {}

    def broadcast(self, clients, message):
        for queue in clients:
            if queue.full():
                continue
            queue.put_nowait(message)

    async def mainLoop(self):
        # FIXME 暂时用这个办法解决队列死锁
        while True:
            await asyncio.sleep(0.01)

    async def main(self):
        # TODO 加入端口配置启动项
        async with websockets.serve(
            self.handler, "0.0.0.0", 8080,
            process_request=self.requestHandler,
            ping_interval=None
        ):
            Log.info("服务器启动完成 - http://localhost:8080")

            await self.mainLoop()

    def run(self):
        asyncio.run(self.main())
