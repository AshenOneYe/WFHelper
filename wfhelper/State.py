import time

from utils.LogUtil import Log


class State:

    content = {
        "startTime": "",
        "lastActionTime": int(time.time()),
        "isRunning": False,
        "currentTargets": "mainTargets",
    }
    callback = None

    def setCallback(self, callback):
        self.callback = callback

    def setState(self, key, value):
        self.content[key] = value
        if self.callback is not None:
            self.callback(self.content)

    def getState(self, key):
        if key in self.content:
            return self.content[key]
        else:
            Log.error("尝试获取不存在的状态值 : {}".format(key))
            return None

    def merge(self, dict):
        self.content.update(dict)

    def has(self, key):
        if key in self.content:
            return True
        return False
