from typing import Any, List


class Target:
    def __init__(self, data: dict) -> None:
        self.name = None
        self.hash = None
        self.text = None
        self.area = None
        self.histogram = None
        self.colorRatio = None
        self.similarityThreshold = None
        self.actions: List[Any] = list()
        self.__dict__ = data
