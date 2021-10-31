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
        

        print("配置文件路径 : {}".format(self.configPath))
        with open(self.configPath, "r",encoding="utf-8") as f:  # 打开文件
            data = f.read()  # 读取文件
            self.targets = json.loads(data)

        if self.targets == None:
            print("读取配置文件出错")
            sys.exit()

        self.picSize = Image.open(configDir + self.targets[0]["path"]).size
        print("屏幕尺寸 : {}x{}".format(self.picSize[0],self.picSize[1]))


        for target in self.targets:
            img = getImageCrop(configDir + target["path"],target["area"])
            target["hash"] = getImageHash(image=img)

