import json
from typing import Dict, Any, List

from os import path

from mergedeep import merge, Strategy
from pathlib import Path

from utils.ImageUtil import getImageCrop, getImageHash
from utils.LogUtil import Log
from .Target import Target


class Config:
    def __init__(self):

        self.name: str = None  # 配置文件名
        self.author: str = None  # 配置文件作者
        self.description: str = None  # 配置文件描述
        self.similarityThreshold: float = 1  # 全局相似度阈值，若有为target单独设置则无视全局阈值
        self.randomClickDelay: float = 300  # 长时间未操作随机点击的触发时间，单位秒
        self.randomClickArea: List[int] = [0, 0, 1, 1]  # 长时间未操作随机点击的点击区域
        self.screenSize: List[int] = None  # 屏幕尺寸
        self.loopDelay: List[float] = [0, 0]  # 每轮循环的延迟时间
        self.configData: Dict[str, Any] = {}
        self.targetList: list = []
        self.state: Dict[str, str] = {}
        self.targetDict: Dict[str, list] = {}

    def setConfigData(self, configData: dict):
        self.configData = configData
        return self

    def init(self):
        self.configDir = path.dirname(self.configData["configPath"])
        self.settingsPath = path.join(self.configDir, "settings.json")
        for key, value in self.configData.items():
            if key in self.__dict__:
                self.__dict__[key] = value

        if not isinstance(self.loopDelay, list):
            loopDelay = self.loopDelay
            self.loopDelay = [loopDelay, loopDelay]

        Log.info("适用屏幕尺寸 : {}x{}".format(self.screenSize[0], self.screenSize[1]))

        # 初始化Targets
        for targetsName in self.configData["targetList"]:
            targetGroup = list()
            targets = self.configData[targetsName]
            for target in targets:
                if "path" in target:
                    img = getImageCrop(
                        path.join(self.configDir, target["path"]), target["area"]
                    )
                    target["hash"] = getImageHash(image=img)
                    if "colorRatio" in target:
                        target["histogram"] = img.histogram()
                t = Target(target)
                targetGroup.append(t)
            self.targetDict[targetsName] = targetGroup

        Log.info("配置文件初始化完成")
        Log.info("配置文件名称 : {}".format(self.name))
        Log.info("配置文件作者 : {}".format(self.author))
        Log.info("配置文件描述 : {}".format(self.description))

    def read_settings(self):
        path = Path(self.settingsPath)

        if path.is_file():
            data = path.read_bytes()

            return json.loads(data)

        return {}

    def merge_settings(self, data):
        path = Path(self.settingsPath)

        source = self.read_settings()

        target = merge({}, source, data, strategy=Strategy.ADDITIVE)

        path.write_bytes(json.dumps(target).encode("utf8"))
