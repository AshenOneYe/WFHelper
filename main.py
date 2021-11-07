import getopt
import sys

from ConfigManager import configManager
from server.Server import Server
from utils.ADBUtil import adbUtil
from utils.LogUtil import Log
from WFHelper import WFHelper
from multiprocessing import Process

if __name__ == "__main__":

    config = None
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
            config = configManager.getConfig(opts["-c"])

            # TODO -v 参数打印log信息
    except getopt.GetoptError:
        Log.error("参数错误")

    if config is None:
        Log.info("未指定配置文件\n")
        config = configManager.selectConfig()
    wfhelper = WFHelper(config)
    # 不用子线程启动的原因是，子线程莫名的速度慢很多
    p = Process(target=wfhelper.run, daemon=True)
    p.start()

    server = Server(wfhelper)
    try:
        server.startServer()
    except KeyboardInterrupt:
        Log.critical("退出!!!")
