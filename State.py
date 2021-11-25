from utils.LogUtil import Log
import time


class State:

    content = {
        "lastActionTime": int(time.time()),
        "isRunning": False,
        "currentTargets": "mainTargets",
    }

    def setState(self, key, value):
        self.content[key] = value

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
