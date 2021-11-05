import json
import sys
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
    configPath = None
    configDir = None
    targets = None
    summary = {}  # type: Dict[str, str]

    def setConfigPath(self, configPath):

        # 在此检查文件是否存在
        try:
            open(configPath, "r", encoding="utf-8")  # 打开文件
            self.configPath = configPath
        except FileNotFoundError:
            try:
                configPath = __file__[0: __file__.rfind("\\") + 1] \
                    + configPath
                open(configPath, "r", encoding="utf-8")  # 打开文件
                self.configPath = configPath
            except FileNotFoundError:
                Log.error("配置文件读取失败，请检查以下文件是否存在:{}".format(configPath))
                sys.exit()

    def updateConfig(self):

        configDir = self.configPath[0: self.configPath.rfind("\\") + 1]
        self.configDir = configDir

        Log.info("配置文件路径 : {}".format(self.configPath))
        try:
            data = open(self.configPath, "r", encoding="utf-8").read()
            self.configData = json.loads(data)
        except json.decoder.JSONDecodeError:
            Log.error("解析配置文件出错，请选择正确的配置文件！")
            sys.exit()

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
        if "targets" in self.configData:
            self.targets = self.configData["targets"]
        if "summary" in self.configData:
            self.summary = self.configData["summary"]

        if self.targets is None:
            Log.error("配置文件读取失败，内容为空")
            sys.exit()

        # 如果不在配置文件中指定屏幕尺寸，则根据配置文件下的截图计算
        if self.screenSize is None:
            self.screenSize = \
                Image.open(configDir + self.targets[0]["path"]).size
        Log.info("屏幕尺寸 : {}x{}".format(self.screenSize[0], self.screenSize[1]))

        for target in self.targets:
            img = getImageCrop(configDir + target["path"], target["area"])
            target["hash"] = getImageHash(image=img)

        Log.info("配置文件初始化完成")
        Log.info("配置文件名称 : {}".format(self.name))
        Log.info("配置文件作者 : {}".format(self.author))
        Log.info("配置文件描述 : {}".format(self.description))

    def __init__(self, configPath=DefaultConfigPath, autoUpdate=True):
        self.setConfigPath(configPath)
        if autoUpdate:
            self.updateConfig()


config = Config(autoUpdate=False)
