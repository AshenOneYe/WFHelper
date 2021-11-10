import json
from typing import Dict

from PIL import Image

from utils.ImageUtil import getImageCrop, getImageHash
from utils.LogUtil import Log

DefaultConfigPath = r"configs\emulator1440x810\config.json"


class Config:

    name = None  # 配置文件名
    author = None  # 配置文件作者
    description = None  # 配置文件描述
    similarityThreshold = 1  # 全局相似度阈值，若有为target单独设置则无视全局阈值
    randomClickDelay = 300  # 长时间未操作随机点击的触发时间，单位秒
    randomClickArea = [0, 0, 1, 1]  # 长时间未操作随机点击的点击区域
    screenSize = None  # 屏幕尺寸
    loopDelay = 0  # 每轮循环的延迟时间
    configData = None
    targetList = {}  # type: Dict[str, list]
    summary = {}  # type: Dict[str, str]

    def __init__(self, configPath=None):

        if configPath is None:
            return

        self.configPath = configPath
        self.configDir = configPath[0: self.configPath.rfind("\\") + 1]

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
            self.loopDelay = self.configData["loopDelay"]
        if "summary" in self.configData:
            self.summary = self.configData["summary"]

        # 如果不在配置文件中指定屏幕尺寸，则根据配置文件下的截图计算
        if self.screenSize is None:
            self.screenSize = \
                Image.open(self.configDir + self.targets[0]["path"]).size
        Log.info("屏幕尺寸 : {}x{}".format(self.screenSize[0], self.screenSize[1]))

        for targetsName in self.configData["targetList"]:
            targets = self.configData[targetsName]
            for target in targets:
                img = getImageCrop(self.configDir + target["path"], target["area"])
                target["hash"] = getImageHash(image=img)
                if "colorRatio" in target:
                    target["histogram"] = img.histogram()
            self.targetList[targetsName] = targets

        Log.info("配置文件初始化完成")
        Log.info("配置文件名称 : {}".format(self.name))
        Log.info("配置文件作者 : {}".format(self.author))
        Log.info("配置文件描述 : {}".format(self.description))
