import getopt
import os
import sys
import threading

from Config import config
from server.Server import Server
from utils.ADBUtil import adbUtil
from utils.LogUtil import Log
from WFHelper import wfhelper

if __name__ == "__main__":

    # https://cloud.tencent.com/developer/article/1739886
    def base_path(path):
        if getattr(sys, "frozen", None):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)
        return os.path.join(basedir, path)

    tmd = base_path("")  # 这是解压路径
    cwd = os.getcwd()  # 这是程序的所在路径
    # 当需要调用打包的外部文件时
    os.chdir(tmd)  # 先把工作路径变成解压路径
    # adb连接
    os.system(r"adb\adb.exe connect 127.0.0.1:7555")
    # 当需要写出文件到程序所在目录时
    os.chdir(cwd)  # 把工作路径切换回来

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:s:c:")
        opts = dict(opts)

        if "-d" in opts:
            device = opts["-d"]
            adbUtil.setDevice(device)
        else:
            adbUtil.setDevice(None)

        if "-s" in opts:
            savePath = opts["-s"]
            Log.info("截图保存至 : {}".format(savePath))
            adbUtil.getScreen(savePath=savePath)
            sys.exit()
        if "-c" in opts:
            config.setConfigPath(opts["-c"])

            # TODO -v 参数打印log信息
    except getopt.GetoptError:
        Log.error("参数错误")

    config.updateConfig()

    server = Server(wfhelper)
    serverThread = threading.Thread(target=server.startServer)
    serverThread.daemon = True
    serverThread.start()

    # 不用子线程启动的原因是，子线程莫名的速度慢很多
    wfhelper.start()
