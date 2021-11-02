import sys
from utils.ImageUtil import *
import json
from PIL import Image
from utils.LogUtil import Log

DefaultConfigPath = "configs\emulator1440x810\config.json"

class Config():

    targets = None
    configPath = None
    configDir = None
    picSize = None


    def setConfigPath(self,configPath):
        
        ## 在此检查文件是否存在
        try:
            open(configPath, "r",encoding="utf-8")  # 打开文件
            self.configPath = configPath
        except FileNotFoundError:
            try:
                configPath = __file__[0:__file__.rfind("\\")+1] + configPath
                open(configPath, "r",encoding="utf-8")  # 打开文件
                self.configPath = configPath
            except FileNotFoundError:
                Log.error("配置文件读取失败，请检查以下文件是否存在:{}".format(configPath))
                sys.exit()


    def updateConfig(self):

        configDir = self.configPath[0:self.configPath.rfind("\\")+1]
        self.configDir = configDir

        Log.info("配置文件路径 : {}".format(self.configPath))
        with open(self.configPath, "r",encoding="utf-8") as f:  # 打开文件
            data = f.read()  # 读取文件
            self.targets = json.loads(data)

        if self.targets == None:
            Log.error("配置文件读取失败，内容为空")
            sys.exit()

        self.picSize = Image.open(configDir + self.targets[0]["path"]).size
        Log.info("屏幕尺寸 : {}x{}".format(self.picSize[0],self.picSize[1]))

        for target in self.targets:
            img = getImageCrop(configDir + target["path"],target["area"])
            target["hash"] = getImageHash(image=img)

        Log.info("配置文件初始化完成")

    def __init__(self,configPath=DefaultConfigPath,autoUpdate=True):
        self.setConfigPath(configPath)
        if autoUpdate:
            self.updateConfig()

config = Config(autoUpdate=False)