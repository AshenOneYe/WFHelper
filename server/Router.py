
import json

from flask import url_for, render_template, redirect, make_response, request
from utils.LogUtil import Log


def setRouter(server):

    app = server.app

    @app.route("/")
    def index():
        return render_template('index.html', log=server.getLastLog())

    @app.route("/getLastLog")
    def getLastLog():
        return server.getLastLog()

    @app.route("/getLogArray")
    def getLogArray():
        return json.dumps(server.getLogArray()).encode('utf8')

    @app.route("/setLogLimit")
    def setLogLimit():
        v = int(request.args.get("value"))
        server.setLogLimit(v)
        return '设置成功'

    @app.route("/getSummary")
    def getSummary():
        return json.dumps(server.getSummary()).encode('utf8')

    @app.route("/getScreenShot")
    def getScreenShot():
        img = server.getScreenShot()
        res = make_response(img)
        res.headers['Content-Type'] = 'image/png'
        return res

    @app.route("/stop")
    def stop():
        server.stopWFHelper()
        return "Stop"

    @app.route("/start")
    def start():
        server.startWFHelper()
        return "Start"

    @app.route("/touchScreen")
    def touchScreen():
        x = int(eval(request.args.get("x")))
        y = int(eval(request.args.get("y")))
        server.touchScreen(x, y)
        return "点击成功"

    @app.route("/swipeScreen")
    def swipeScreen():
        x1 = int(eval(request.args.get("x1")))
        y1 = int(eval(request.args.get("y1")))
        x2 = int(eval(request.args.get("x2")))
        y2 = int(eval(request.args.get("y2")))
        server.swipeScreen(x1, y1, x2, y2)
        return "滑动成功"

    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('favicon.ico')

    @app.errorhandler(404)
    def page_not_found(error):
        return redirect(url_for('index'))

    Log.info("服务器初始化完成")
