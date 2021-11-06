import json
import os
import sys

from Config import Config


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
            if "name" in config.configData and "author" in config.configData and "description" in config.configData:
                return config
        except json.decoder.JSONDecodeError:
            print("发现一个格式错误的配置文件 : {}".format(configPath))
        return None

    def selectConfig(self):
        configs = self.getConfigs()
        if len(configs) == 0:
            input("\n没有找到任何配置文件，按回车键退出")
            sys.exit()
        print("\n请选择一个配置文件，默认选择第一个:")
        index = 0
        for config in configs:
            print("\n[{}] - {}".format(index, config.configPath))
            print("\t名称 : - {}".format(config.configData["name"]))
            print("\t作者 : - {}".format(config.configData["author"]))
            print("\t描述 : - {}".format(config.configData["description"]))
            index += 1

        i = int(input())
        config = configs[i]
        return config


configManager = ConfigManager()
