import getopt
import sys
import multiprocessing

from utils.ConfigUtil import configUtil
from utils.ADBUtil import adbUtil
from utils.LogUtil import Log
from wfhelper.WFHelperWrapper import WFHelperWrapper
from server.Server import Server

if __name__ == "__main__":
    # 不写这个打包exe会出问题
    multiprocessing.freeze_support()

    isDebug = False

    serial = None
    config = None

    instance = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "-t-s:-d:-c:-n")
        opts = dict(opts)

        if "-t" in opts:
            isDebug = True

        if "-s" in opts:
            savePath = opts["-s"]
            adbUtil.getScreen(savePath)
            Log.info("截图保存至 : {}".format(savePath))
            sys.exit()

        if "-d" in opts:
            serial = opts["-d"]

        if "-c" in opts:
            config = configUtil.getConfig(opts["-c"])
    
        if "-n" in opts:
            instance = WFHelperWrapper(serial, config)

        # TODO -v 参数打印log信息
    except getopt.GetoptError:
        Log.error("参数错误")

    # 指定了设备、配置时创建WFHelper实例
    if serial is not None or config is not None:
        instance = WFHelperWrapper(serial, config)

    server = Server(instance, isDebug)
    server.run()