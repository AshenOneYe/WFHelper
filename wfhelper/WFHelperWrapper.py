import threading
from multiprocessing import Pipe, Process

from utils import Log, adbUtil

from .WFHelper import WFHelper


class WFHelperWrapper(Process):

    config = None

    receivingThread = None
    childConn = None
    parentConn = None

    eventHandlerThread = None
    childEventConn = None
    parentEventConn = None

    frameThread = None

    isChild = False

    def __init__(self, serial: str, config):
        super().__init__()
        self.daemon = True
        self.serial = serial
        self.config = config
        self.childConn, self.parentConn = Pipe()
        self.childEventConn, self.parentEventConn = Pipe()

        self.wfhelper = WFHelper()

    def run(self):
        self.init()
        self.wfhelper.run()

    def init(self):
        self.isChild = True
        self.config.init()
        self.wfhelper.setConfig(self.config)
        self.wfhelper.state.setCallback(self.onStateUpdate)

        self.receivingThread = threading.Thread(
            target=self.onChildReceive, args=(self.childConn,)
        )
        self.receivingThread.daemon = True
        self.receivingThread.start()

        self.frameThread = threading.Thread(target=self.frameLoop)
        self.frameThread.daemon = True
        self.frameThread.start()

        # TODO 现在多个实例共用同一个serial，应该分离
        adbUtil.setDevice(self.serial)
        Log.onLogAppend(self.onLogAppend)

    def frameLoop(self):
        while True:
            frame = adbUtil.getScreen()

            if frame is not None:
                self.onFrameUpdate(frame)
                self.wfhelper.lastFrame = frame

    def emit(self, type, data):
        self.childEventConn.send({"type": type, "data": data})

    def setEventHandler(self, handler):
        def waitForEvent():
            while True:
                try:
                    event = self.parentEventConn.recv()
                    handler(event)
                except Exception:
                    continue

        self.eventHandlerThread = threading.Thread(target=waitForEvent)
        self.eventHandlerThread.daemon = True
        self.eventHandlerThread.start()

    def onChildReceive(self, conn):
        while True:
            msg = conn.recv()
            if "args" in msg:
                getattr(self, msg["method"])(args=msg["args"])
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
            self.parentConn.send({"method": "setState", "args": args})

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
            self.parentConn.send({"method": "setLogLimit", "args": args})

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
            adbUtil.touchScreen([args["x"], args["y"], args["x"] + 1, args["y"] + 1])
        else:
            self.parentConn.send({"method": "touchScreen", "args": args})

    def swipeScreen(self, args):
        if self.isChild:
            adbUtil.swipeScreen(args["x1"], args["y1"], args["x2"], args["y2"])
        else:
            self.parentConn.send({"method": "swipeScreen", "args": args})
