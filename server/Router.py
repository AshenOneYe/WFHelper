from flask import url_for,render_template,redirect,make_response

def setRouter(server):

    app = server.app

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/getLastLog")
    def getLastLog():
        return server.getLastLog()

    @app.route("/getScreenShot")
    def getScreenShot():
        img = server.getScreenShot()
        res = make_response(img)
        res.headers['Content-Type'] = 'image/png'
        return res

    @app.errorhandler(404)
    def page_not_found(error):
        return redirect(url_for('index'))

    server.main.log("服务器初始化完成")