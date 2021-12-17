import json
import os
import sys
from typing import List, Union

rootPath = "configs"


def getConfigFileList() -> List[str]:
    configFileList = []
    for root, dirs, files in os.walk(rootPath):
        for file in files:
            if file == "config.json":
                configFileList.append(os.path.join(root, file))
    return configFileList


def getConfigs() -> List[dict]:
    configs = []
    for configFile in getConfigFileList():
        config = getConfig(configFile)
        if config is not None:
            configs.append(config)
    return configs


def getConfig(configPath: str) -> Union[dict, None]:
    try:
        with open(configPath, "r", encoding="utf-8") as file:
            config: dict = json.loads(file.read())
            if "name" in config and "author" in config and "description" in config:
                config["configPath"] = configPath
                return config
    except json.decoder.JSONDecodeError:
        print("发现一个格式错误的配置文件 : {}".format(configPath))
    return None


def selectConfig() -> dict:
    configs = getConfigs()
    if len(configs) == 0:
        input("\n没有找到任何配置文件，按回车键退出")
        sys.exit()
    print("\n请选择一个配置文件，默认选择第一个:")
    index = 0
    for config in configs:
        print("\n[{}] - {}".format(index, config["configPath"]))
        print("\t名称 : - {}".format(config["name"]))
        print("\t作者 : - {}".format(config["author"]))
        print("\t描述 : - {}".format(config["description"]))
        index += 1

    i: int = int(input())
    if i is None or i == "":
        i = 0
    try:
        i = int(i)
        config = configs[i]
        return config
    except ValueError:
        print("输入的序号有误!")
        sys.exit()
