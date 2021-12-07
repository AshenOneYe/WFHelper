from utils.LogUtil import Log


def setWebSocket(server):
    socketio = server.socketio

    @socketio.on('connect')
    def onConnect(auth):
        Log.debug("websocket Client connected!")

    @socketio.on('disconnect')
    def onDisonnect():
        Log.debug("websocket Client disconnected!")
