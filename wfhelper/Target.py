from typing import Any, List


class Target:
    def __init__(self, data: dict) -> None:
        self.name = None
        self.hash = None
        self.text = None
        self.area = None
        self.histogram = None
        self.colorRatio = 0
        self.description = None
        self.similarityThreshold = None
        self.actions: List[Any] = list()

        for key, value in data.items():
            if key in self.__dict__:
                self.__dict__[key] = value
