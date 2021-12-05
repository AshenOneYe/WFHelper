from WFHelper import WFHelper
from multiprocessing import Process
import Connection
from utils.ADBUtil import adbUtil
from utils.LogUtil import Log


class WFHelperWrapper(Process):

    wfhelper = WFHelper()

    recvConn = None
    sendConn = None

    config = None
    serial = None
    isDebug = False

    def __init__(self, config, serial, isDebug):
        super().__init__()
        self.daemon = True
        self.config = config
        self.serial = serial
        self.isDebug = isDebug

        self.recvConn, self.sendConn = Connection.getConnections()

    def init(self):
        self.recvConn.setCallback(self.onMessage)
        self.recvConn.startReceive()
        self.config.init()
        self.wfhelper.setConfig(self.config)
        self.wfhelper.enableDebug(self.isDebug)
        adbUtil.setDevice(self.serial, True)

    def run(self):
        self.init()
        self.wfhelper.run()

    def onMessage(self, msg):
        if msg["type"] == "getState":
            self.recvConn.send(self.wfhelper.state.content)
        elif msg["type"] == "setState":
            self.wfhelper.state.setState(msg["key"], msg["value"])
        elif msg["type"] == "getLastLog":
            self.recvConn.send(Log.lastLog)
        elif msg["type"] == "getLogArray":
            self.recvConn.send(Log.logArray)
        elif msg["type"] == "setLogLimit":
            Log.logArray = []
            Log.logLimit = msg["value"]
        elif msg["type"] == "getScreenShot":
            self.recvConn.send(Log.lastLog)
        elif msg["type"] == "touchScreen":
            x, y = msg["pos"]
            adbUtil.touchScreen([x, y, x+1, y+1])
        elif msg["type"] == "swipeScreen":
            x1, y1 = msg["start"]
            x2, y2 = msg["end"]
            adbUtil.swipeScreen(x1, y1, x2, y2)
        elif msg["type"] == "stopWFHelper":
            self.wfhelper.stop()
        elif msg["type"] == "startWFHelper":
            self.wfhelper.start()

    def getState(self):
        return self.sendConn.getResponse({"type": "getState"})

    def setState(self, key, value):
        self.sendConn.send({
            "type": "getLogArray",
            "key": key,
            "value": value
        })

    def getLastLog(self):
        return self.sendConn.getResponse({"type": "getLastLog"})

    def getLogArray(self):
        return self.sendConn.getResponse({"type": "getLogArray"})

    def setLogLimit(self, value):
        self.sendConn.send({
            "type": "setLogLimit",
            "value": value
        })

    def getScreenShot(self):
        return adbUtil.getScreen()

    def touchScreen(self, x, y):
        self.sendConn.send({
            "type": "touchScreen",
            "x": x,
            "y": y
        })

    def swipeScreen(self, x1, y1, x2, y2):
        self.sendConn.send({
            "type": "swipeScreen",
            "start": [x1, y1],
            "end": [x2, y2]
        })

    def stopWFHelper(self):
        self.sendConn.send("stopWFHelper")

    def startWFHelper(self):
        self.sendConn.send("startWFHelper")
