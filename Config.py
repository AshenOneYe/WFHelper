import sys
from utils.ImageUtil import *
import json
from PIL import Image

class Config():

    targets = None
    configPath = "configs\emulator1440x810\config.json"
    configDir = None
    picSize = None

    def __init__(self,configPath=None):

        if configPath != None:
            self.configPath = configPath
        configDir = self.configPath[0:self.configPath.rfind("\\")+1]
        

        with open(self.configPath, "r",encoding="utf-8") as f:  # 打开文件
            data = f.read()  # 读取文件
            self.targets = json.loads(data)

        if self.targets == None:
            print("配置文件出错")
            sys.exit()

        self.picSize = Image.open(configDir + self.targets[0]["path"]).size

        for target in self.targets:
            img = getImageCrop(configDir + target["path"],target["area"])
            target["hash"] = getImageHash(image=img)

