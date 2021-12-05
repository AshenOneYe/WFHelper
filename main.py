import getopt
import sys

from utils.ConfigUtil import configUtil
from wfhelper.WFHelperWrapper import WFHelperWrapper
from server.Server import Server
from utils.ADBUtil import adbUtil
from utils.LogUtil import Log


if __name__ == "__main__":

    isDebug = False
    config = None
    serial = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:s:c:t")
        opts = dict(opts)

        if "-d" in opts:
            serial = opts["-d"]
            adbUtil.setDevice(serial)
        else:
            serial = adbUtil.setDevice(None)

        if "-s" in opts:
            savePath = opts["-s"]
            Log.info("截图保存至 : {}".format(savePath))
            adbUtil.getScreen(savePath=savePath)
            sys.exit()

        if "-c" in opts:
            config = configUtil.getConfig(opts["-c"])

        if "-t" in opts:
            isDebug = True

            # TODO -v 参数打印log信息
    except getopt.GetoptError:
        Log.error("参数错误")

    if config is None:
        Log.info("未指定配置文件\n")
        config = configUtil.selectConfig()

    wfhelper = WFHelperWrapper(config, serial, isDebug)
    wfhelper.start()

    Server(wfhelper).startServer()
