import json
from typing import Dict, Any
from os import path

from utils.ImageUtil import getImageCrop, getImageHash
from utils.LogUtil import Log


class Config:
    def __init__(self, configPath: str = None):

        if configPath is None:
            return

        self.name = None  # 配置文件名
        self.author = None  # 配置文件作者
        self.description = None  # 配置文件描述
        self.similarityThreshold = 1  # 全局相似度阈值，若有为target单独设置则无视全局阈值
        self.randomClickDelay = 300  # 长时间未操作随机点击的触发时间，单位秒
        self.randomClickArea = [0, 0, 1, 1]  # 长时间未操作随机点击的点击区域
        self.screenSize = None  # 屏幕尺寸
        self.loopDelay = [0, 0]  # 每轮循环的延迟时间
        self.configData = {}  # type: Dict[str, Any]
        self.targetList = {}  # type: Dict[str, list]
        self.state = {}  # type: Dict[str, str]

        self.configPath = configPath
        self.configDir = path.dirname(configPath)

        data = open(self.configPath, "r", encoding="utf-8").read()
        self.configData = json.loads(data)

    def init(self):
        if "name" in self.configData:
            self.name = self.configData["name"]
        if "author" in self.configData:
            self.author = self.configData["author"]
        if "description" in self.configData:
            self.description = self.configData["description"]
        if "similarityThreshold" in self.configData:
            self.similarityThreshold = self.configData["similarityThreshold"]
        if "randomClickDelay" in self.configData:
            self.randomClickDelay = self.configData["randomClickDelay"]
        if "randomClickArea" in self.configData:
            self.randomClickArea = self.configData["randomClickArea"]
        if "screenSize" in self.configData:
            self.screenSize = self.configData["screenSize"]
        if "loopDelay" in self.configData:
            if isinstance(self.configData["loopDelay"], list):
                self.loopDelay = self.configData["loopDelay"]
            else:
                loopDelay = self.configData["loopDelay"]
                self.loopDelay = [loopDelay, loopDelay]
        if "state" in self.configData:
            self.state = self.configData["state"]

        Log.info("适用屏幕尺寸 : {}x{}".format(self.screenSize[0], self.screenSize[1]))

        for targetsName in self.configData["targetList"]:
            targets = self.configData[targetsName]
            for target in targets:
                if "path" in target:
                    img = getImageCrop(
                        path.join(self.configDir, target["path"]), target["area"]
                    )
                    target["hash"] = getImageHash(image=img)
                    if "colorRatio" in target:
                        target["histogram"] = img.histogram()
            self.targetList[targetsName] = targets

        Log.info("配置文件初始化完成")
        Log.info("配置文件名称 : {}".format(self.name))
        Log.info("配置文件作者 : {}".format(self.author))
        Log.info("配置文件描述 : {}".format(self.description))
