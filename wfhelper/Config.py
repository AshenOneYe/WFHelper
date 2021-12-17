from typing import Dict, Any, List, Optional
from os import path

from utils.ImageUtil import getImageCrop, getImageHash
from utils.LogUtil import Log


class Config:
    def __init__(self):

        self._name: str = None  # 配置文件名
        self._author: str = None  # 配置文件作者
        self._description: str = None  # 配置文件描述
        self.similarityThreshold: float = 1  # 全局相似度阈值，若有为target单独设置则无视全局阈值
        self.randomClickDelay: float = 300  # 长时间未操作随机点击的触发时间，单位秒
        self.randomClickArea: List[int] = [0, 0, 1, 1]  # 长时间未操作随机点击的点击区域
        self.screenSize: List[int] = None  # 屏幕尺寸
        self.loopDelay: List[float] = [0, 0]  # 每轮循环的延迟时间
        self._configData: Dict[str, Any] = {}
        self.targetList: Dict[str, list] = {}
        self.state: Dict[str, str] = {}
        self._configPath: Optional[str] = None
        self._configDir: Optional[str] = None

    def setConfigData(self, configData: dict):
        self._configData = configData
        return self

    def init(self):
        self._configPath = self._configData["configPath"]
        self._configDir = path.dirname(self._configPath)

        if "name" in self._configData:
            self._name = self._configData["name"]
        if "author" in self._configData:
            self._author = self._configData["author"]
        if "description" in self._configData:
            self._description = self._configData["description"]
        if "similarityThreshold" in self._configData:
            self.similarityThreshold = self._configData["similarityThreshold"]
        if "randomClickDelay" in self._configData:
            self.randomClickDelay = self._configData["randomClickDelay"]
        if "randomClickArea" in self._configData:
            self.randomClickArea = self._configData["randomClickArea"]
        if "screenSize" in self._configData:
            self.screenSize = self._configData["screenSize"]
        if "loopDelay" in self._configData:
            if isinstance(self._configData["loopDelay"], list):
                self.loopDelay = self._configData["loopDelay"]
            else:
                loopDelay = self._configData["loopDelay"]
                self.loopDelay = [loopDelay, loopDelay]
        if "state" in self._configData:
            self.state = self._configData["state"]

        Log.info("适用屏幕尺寸 : {}x{}".format(self.screenSize[0], self.screenSize[1]))

        # 初始化Targets
        for targetsName in self._configData["targetList"]:
            targets = self._configData[targetsName]
            for target in targets:
                if "path" in target:
                    img = getImageCrop(
                        path.join(self._configDir, target["path"]), target["area"]
                    )
                    target["hash"] = getImageHash(image=img)
                    if "colorRatio" in target:
                        target["histogram"] = img.histogram()
            self.targetList[targetsName] = targets

        Log.info("配置文件初始化完成")
        Log.info("配置文件名称 : {}".format(self._name))
        Log.info("配置文件作者 : {}".format(self._author))
        Log.info("配置文件描述 : {}".format(self._description))
