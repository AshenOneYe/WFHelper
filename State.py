import json
import time

from utils.LogUtil import Log
from utils.WSUtil import WS


class State:

    content = {
        "startTime": "",
        "lastActionTime": int(time.time()),
        "isRunning": False,
        "currentTargets": "mainTargets",
    }

    def setState(self, key, value):
        self.content[key] = value
        self.broadcast()

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

    def broadcast(self):
        WS.broadcast(json.dumps({
            "type": 'update-state',
            "time": int(time.time()),
            "data": self.content
        }).encode('utf8'))
