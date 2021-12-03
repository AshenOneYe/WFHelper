from flask import Flask
from server.Router import setRouter
from utils.ADBUtil import adbUtil
from utils.LogUtil import Log
from server.WebSocket import setWebSocket
from flask_socketio import SocketIO


class Server():
    app = Flask(__name__)
    wfhelper = None
    socketio = SocketIO(app)

    def __init__(self, wfhelper):

        # TODO 提供参数指定host和port
        self.wfhelper = wfhelper
        setRouter(self)
        setWebSocket(self)

    def getLastLog(self):
        return Log.lastLog

    def getLogArray(self):
        return Log.logArray

    def setLogLimit(self, value):
        Log.logArray = []
        Log.logLimit = value

    def setState(self, key, value):
        self.wfhelper.state.setState(key, value)

    def getState(self):
        return self.wfhelper.state.content

    def getScreenShot(self):
        return adbUtil.getScreen()

    def touchScreen(self, x, y):
        adbUtil.touchScreen([x, y, x+1, y+1])

    def swipeScreen(self, x1, y1, x2, y2):
        adbUtil.swipeScreen(x1, y1, x2, y2)

    def stopWFHelper(self):
        self.wfhelper.stop()

    def startWFHelper(self):
        self.wfhelper.start()

    def startServer(self):
        self.socketio.run(self.app, "0.0.0.0", 8080)
        # from gevent import pywsgi
        # from geventwebsocket.handler import WebSocketHandler
        # server = pywsgi.WSGIServer(('', 8080), self.app, handler_class=WebSocketHandler)
        # server.serve_forever()
