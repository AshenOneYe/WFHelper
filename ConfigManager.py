import os
from Config import Config
import json


class ConfigManager:
    rootPath = "configs"

    def getConfigFileList(self):
        configFileList = []
        for root, dirs, files in os.walk(self.rootPath):
            for dir in dirs:
                configDir = os.path.join(root, dir)
                for r, d, files in os.walk(configDir):
                    for f in files:
                        if f == "config.json":
                            configFileList.append(os.path.join(r, f))
        return configFileList

    def getConfigs(self):
        configs = []
        for configFile in self.getConfigFileList():
            config = self.getConfig(configFile)
            if config is not None:
                configs.append(config)
        return configs

    def getConfig(self, configPath):
        try:
            config = Config(configPath)
            return config
        except json.decoder.JSONDecodeError:
            print("发现一个格式错误的配置文件 : {}".format(configPath))
        return None

    def selectConfig(self):
        configs = self.getConfigs()
        print("\n请选择一个配置文件，默认选择第一个:")
        for i in range(0, len(configs)):
            config = configs[i]
            print("\n[{}] - {}".format(i, config.configPath))
            print("\t名称 : - {}".format(config.configData["name"]))
            print("\t作者 : - {}".format(config.configData["author"]))
            print("\t描述 : - {}".format(config.configData["description"]))
        i = int(input())
        config = configs[i]
        return config


configManager = ConfigManager()
