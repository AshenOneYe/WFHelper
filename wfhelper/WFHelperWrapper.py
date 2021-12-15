import asyncio
import json
from wfhelper.WFHelper import WFHelper
from multiprocessing import Pipe, Process
from utils.ADBUtil import adbUtil
from utils.ConfigUtil import configUtil
from utils.LogUtil import Log
import threading

class WFHelperWrapper(Process):

    wfhelper = WFHelper()

    serial = None
    config = None

    receivingThread = None
    childConn = None
    parentConn = None

    eventHandlerThread = None
    childEventConn = None
    parentEventConn = None

    isChild = False

    def __init__(self, serial = None, config = None):
        super().__init__()
        self.daemon = True

        # FIXME 现在多个实例共用同一个serial，应该分离
        self.serial = adbUtil.setDevice(serial)

        if config is None:
            self.config = configUtil.selectConfig()
        else:
            self.config = config

        self.childConn, self.parentConn = Pipe()
        self.childEventConn, self.parentEventConn = Pipe()


    def run(self):
        self.init()
        self.wfhelper.run()

    def init(self):
        self.isChild = True

        self.config.init()
        self.wfhelper.setConfig(self.config)
        self.wfhelper.screenUpdateCallback = self.onFrameUpdate
        self.wfhelper.state.setCallback(self.onStateUpdate)

        self.receivingThread = threading.Thread(target = self.onChildReceive, args = (self.childConn,))
        self.receivingThread.daemon = True
        self.receivingThread.start()

        adbUtil.setDevice(self.serial)
        Log.onLogAppend(self.onLogAppend)

    def emit(self, type, data):
        self.childEventConn.send({
            "type": type,
            "data": data
        })

    def setEventHandler(self, handler):
        def eventLoop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(waitForEvent())
            loop.close()

        async def waitForEvent():
            while True:
                event = self.parentEventConn.recv()
                await handler(event)

        self.eventHandlerThread = threading.Thread(target = eventLoop)
        self.eventHandlerThread.daemon = True
        self.eventHandlerThread.start()

    def onChildReceive(self, conn):
        while True:
            msg = conn.recv()
            if "args" in msg:
                getattr(self, msg["method"])(args = msg["args"])
            else:
                getattr(self, msg["method"])()

    def onLogAppend(self, log):
        self.emit("onLogAppend", log)

    def onStateUpdate(self, state):
        self.emit("onStateUpdate", state)

    def onFrameUpdate(self, frame):
        self.emit("onFrameUpdate", frame)

    def getState(self):
        if self.isChild:
            self.childConn.send(self.wfhelper.state.content)
        else:
            self.parentConn.send({"method": "getState"})
            return self.parentConn.recv()

    def setState(self, args):
        if self.isChild:
            self.wfhelper.state.setState(args["key"], args["value"])
        else:
            self.parentConn.send({
                "method": "setState",
                "args": args
            })

    def getLogArray(self):
        if self.isChild:
            self.childConn.send(Log.logArray)
        else:
            self.parentConn.send({ 
                "method": "getLogArray"
            })
            return self.parentConn.recv()

    def setLogLimit(self, args):
        if self.isChild:
            Log.logArray = []
            Log.logLimit = args
        else:
            self.parentConn.send({
                "method": "setLogLimit",
                "args": args
            })

    def startWFHelper(self):
        if self.isChild:
            self.wfhelper.start()
        else:
            self.parentConn.send({"method": "startWFHelper"})

    def stopWFHelper(self):
        if self.isChild:
            self.wfhelper.stop()
        else:
            self.parentConn.send({"method": "stopWFHelper"})

    def touchScreen(self, args):
        if self.isChild:
            adbUtil.touchScreen([
                args["x"], args["y"],
                args["x"] + 1, args["y"] + 1])
        else:
            self.parentConn.send({
                "method": "touchScreen",
                "args": args
            })

    def swipeScreen(self, args):
        if self.isChild:
            adbUtil.swipeScreen(
                args["x1"], args["y1"],
                args["x2"], args["y2"]
            )
        else:
            self.parentConn.send({
                "method": "swipeScreen",
                "args": args
            })
