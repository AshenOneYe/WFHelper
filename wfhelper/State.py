import time
from typing import Any, Callable, Dict, List

from utils import Log


class State:

    def __init__(self) -> None:
        self.content = {
            "startTime": "",
            "lastActionTime": int(time.time()),
            "isRunning": False,
            "currentTargets": "mainTargets",
        }
        self.callbacks: List[Callable] = []

    def addCallback(self, callback: Callable[..., Any]):
        self.callbacks.append(callback)

    def setState(self, key: str, value: Any):
        self.content[key] = value
        for func in self.callbacks:
            func(self.content)

    def getState(self, key: str):
        if key in self.content:
            return self.content[key]
        else:
            Log.info("尝试获取不存在的状态值 : {}".format(key))
            return None

    def merge(self, dict: Dict[str, Any]):
        self.content.update(dict)

    def has(self, key: str):
        if key in self.content:
            return True
        return False
