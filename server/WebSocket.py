from flask_sockets import Sockets


def setWebSocket(server):
    app = server.app
    sockets = Sockets(app)

    @sockets.route('/echo')
    def echo_socket(ws):
        ws.send("test")
