from flask import Flask
from wsgiref.simple_server import make_server
from server.Router import setRouter
from utils.ADBUtil import adbUtil


class Server():
    app = Flask(__name__)
    main = None

    def __init__(self,main):

        # TODO 提供参数指定host和port

        self.main = main
        setRouter(self)


    def getLastLog(self):
        return self.main.lastLog

    def getScreenShot(self):
        return adbUtil.getScreen()

    def touchScreen(self,x,y):
        adbUtil.touchScreen([x,y,x+1,y+1])


    def startServer(self):
        server = make_server('', 8080,self.app)
        server.serve_forever()
        # self.app.run("0.0.0.0",8080,debug=False)

        
