import getopt
import sys
import threading

from Config import config
from server.Server import Server
from utils.ADBUtil import adbUtil
from utils.LogUtil import Log
from WFHelper import wfhelper

if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:s:c:")
        opts = dict(opts)

        if "-d" in opts:
            serial = opts["-d"]
            adbUtil.setDevice(serial)
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
    wfhelper.init()
