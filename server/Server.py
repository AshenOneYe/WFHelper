import asyncio
import http
import json
import logging
import websockets
from os.path import splitext
from pathlib import Path
from utils.LogUtil import Log
from wfhelper.WFHelperWrapper import WFHelperWrapper

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

    instances = set()

    clients = set()
    streamClients = set()

    def __init__(self, instance = None, isDebug = False):
        if isDebug:
            Log.setDebugLevel()

            self.isDebug = isDebug

        if instance is not None:
            self.createInstance(instance)

        # FIXME 为避免其他使用者造成疑惑，当前版本默认创建实例并给出警告
        if instance is None:
            Log.warning("脚本将在未来版本中取消默认启动任务并在UI中统一管理，如有需要请使用 -n 指令")
            
            self.createInstance()

    def createInstance(self, instance = None):
        if instance is None:
            instance = WFHelperWrapper()
            
        instance.start()
        instance.setState({
            "key": "isDebug",
            "value": self.isDebug
        })
        instance.setEventHandler(self.eventHandler)

        self.instances.add(instance)

    async def handler(self, websocket, path):
        self.bindClient(websocket, path)

        try:
            async for message in websocket:
                await self.messageHandler(message, websocket, path)
        finally:
            self.unbindClient(websocket, path)

    async def messageHandler(self, message, websocket, path):
        try:
            message = json.loads(message)

            # FIXME 现在强制使用单例模式，应读取websocket对应实例
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
        except:
            pass

    async def eventHandler(self, event):
        type = event["type"]

        # TODO 也应发送给对应实例
        if type == "onLogAppend" or type == "onStateUpdate":
            self.broadcastClients(
                json.dumps({
                    "type": type,
                    "data": event["data"]
                }).encode('utf8')
            )
        elif type == "onFrameUpdate":
            self.broadcastStreamClients(event["data"])

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

    def bindClient(self, websocket, path):
        if path == "/websocket":
            self.clients.add(websocket)
        if path == "/stream":
            self.streamClients.add(websocket)
        
    def unbindClient(self, websocket, path):
        if path == "/websocket":
            self.clients.remove(websocket)
        if path == "/stream":
            self.streamClients.remove(websocket)

    def broadcastClients(self, message):
        try:
            websockets.broadcast(self.clients, message)
        except:
            pass

    def broadcastStreamClients(self, message):
        try:
            websockets.broadcast(self.streamClients, message)
        except:
            pass

    async def main(self):
        # TODO 加入端口配置启动项
        async with websockets.serve(
            self.handler, "0.0.0.0", 8080, 
            process_request = self.requestHandler
        ):
            Log.info("服务器启动完成 - http://localhost:8080")
            await asyncio.Future() 

    def run(self):
        asyncio.run(self.main())