from utils.LogUtil import Log


def setWebSocket(server):
    socketio = server.socketio

    @socketio.on('connect')
    def onConnect(auth):
        Log.info("websocket Client connected!")

    @socketio.on('disconnect')
    def onDisonnect():
        Log.info("websocket Client disconnected!")
        # stopThread
