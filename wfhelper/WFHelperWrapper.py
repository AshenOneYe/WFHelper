from wfhelper.WFHelper import WFHelper
from multiprocessing import Pipe, Process
from utils.ADBUtil import adbUtil
from utils.LogUtil import Log
import threading
import base64


class WFHelperWrapper(Process):

    wfhelper = WFHelper()

    childConn = None
    parentConn = None
    childEventConn = None
    parentEventConn = None
    receivingThread = None
    eventHandlerThread = None
    config = None
    serial = None
    isDebug = False
    isChild = False

    def __init__(self, config, serial, isDebug):
        super().__init__()
        self.daemon = True
        self.config = config
        self.serial = serial
        self.isDebug = isDebug
        self.childConn, self.parentConn = Pipe()
        self.childEventConn, self.parentEventConn = Pipe()

    def init(self):
        self.isChild = True
        self.config.init()
        self.wfhelper.setConfig(self.config)
        self.wfhelper.enableDebug(self.isDebug)
        self.wfhelper.screenUpdateCallback = self.updateFrame
        self.wfhelper.state.setCallback(self.updateState)
        Log.setCallback(self.updateLog)
        adbUtil.setDevice(self.serial, True)
        self.receivingThread = threading.Thread(target=self.onChildReceive, args=(self.childConn,))
        self.receivingThread.daemon = True
        self.receivingThread.start()

    def updateFrame(self, frame):
        self.emit({"type": "onFrameUpdate", "data": base64.b64encode(frame).decode("utf-8")})

    def updateState(self, state):
        self.emit({"type": "onStateUpdate", "data": state})

    def updateLog(self, log):
        self.emit({"type": "onLogUpdate", "data": log})

    def emit(self, event):
        self.childEventConn.send(event)

    def setEventHandler(self, handler):
        def waitForEvent():
            while True:
                event = self.parentEventConn.recv()
                handler(event)
        self.eventHandlerThread = threading.Thread(target=waitForEvent)
        self.eventHandlerThread.daemon = True
        self.eventHandlerThread.start()

    def run(self):
        self.init()
        self.wfhelper.run()

    def onChildReceive(self, conn):
        while True:
            msg = conn.recv()
            if "args" in msg:
                getattr(self, msg["method"])(args=msg["args"])
            else:
                getattr(self, msg["method"])()

    def getState(self):
        if self.isChild:
            self.childConn.send(self.wfhelper.state.content)
        else:
            self.parentConn.send({"method": "getState"})
            return self.parentConn.recv()

    def setState(self, args):
        if self.isChild:
            key, value = args
            self.wfhelper.state.setState(key, value)
        else:
            self.parentConn.send({
                "method": "setState",
                "args": args
            })

    def getLastLog(self):
        if self.isChild:
            self.childConn.send(Log.lastLog)
        else:
            self.parentConn.send({"method": "getLastLog"})
            return self.parentConn.recv()

    def getLogArray(self):
        if self.isChild:
            self.childConn.send(Log.logArray)
        else:
            self.parentConn.send({"method": "getLogArray"})
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

    def getScreenShot(self):
        if self.isChild:
            self.childConn.send(self.frame)
        else:
            self.parentConn.send({"method": "getScreenShot"})
            return self.parentConn.recv()

    def touchScreen(self, args):
        if self.isChild:
            x, y = args
            adbUtil.touchScreen([x, y, x+1, y+1])
        else:
            self.parentConn.send({
                "method": "touchScreen",
                "args": args
            })

    def swipeScreen(self, args):
        if self.isChild:
            x1, y1, x2, y2 = args
            adbUtil.swipeScreen(x1, y1, x2, y2)
        else:
            self.parentConn.send({
                "method": "swipeScreen",
                "args": args
            })

    def stopWFHelper(self):
        if self.isChild:
            self.wfhelper.stop()
        else:
            self.parentConn.send({"method": "stopWFHelper"})

    def startWFHelper(self):
        if self.isChild:
            self.wfhelper.start()
        else:
            self.parentConn.send({"method": "startWFHelper"})
