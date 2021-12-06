from flask import Flask
from server.Router import setRouter
from server.WebSocket import setWebSocket
from flask_socketio import SocketIO


class Server():
    app = Flask(__name__)
    wfhelper = None
    socketio = SocketIO(app, cors_allowed_origins='*')

    def eventHandler(self, event):
        self.socketio.emit(event["type"], event["data"])

    def __init__(self, wfhelper):

        # TODO 提供参数指定host和port
        self.wfhelper = wfhelper
        self.wfhelper.setEventHandler(self.eventHandler)
        setRouter(self)
        setWebSocket(self)

    def getLastLog(self):
        return self.wfhelper.getLastLog()

    def getLogArray(self):
        return self.wfhelper.getLogArray()

    def setLogLimit(self, value):
        self.wfhelper.setLogLimit(value)

    def setState(self, key, value):
        self.wfhelper.setState([key, value])

    def getState(self):
        return self.wfhelper.getState()

    def getScreenShot(self):
        return self.wfhelper.getScreenShot()

    def touchScreen(self, x, y):
        self.wfhelper.touchScreen([x, y])

    def swipeScreen(self, x1, y1, x2, y2):
        self.wfhelper.swipeScreen([x1, y1, x2, y2])

    def stopWFHelper(self):
        self.wfhelper.stopWFHelper()

    def startWFHelper(self):
        self.wfhelper.startWFHelper()

    def startServer(self):
        self.socketio.run(self.app, "0.0.0.0", 8080)
        # from gevent import pywsgi
        # from geventwebsocket.handler import WebSocketHandler
        # server = pywsgi.WSGIServer(('', 8080), self.app, handler_class=WebSocketHandler)
        # server.serve_forever()
