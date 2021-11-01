from Config import config
from server.Server import Server
from utils.ADBUtil import adbUtil
import sys
import getopt
import threading
from utils.LogUtil import Log
from WFHelper import wfhelper

if __name__ == '__main__':

    try:
        opts,args = getopt.getopt(sys.argv[1:], "d:s:c:")
        
        for o,a in opts:
            if o == "-d":
                Log.info("设备名 : {}".format(a))
                adbUtil.setDevice(a)
            elif o == "-s":
                Log.info("截图保存至 : {}".format(a))
                adbUtil.getScreen(savePath=a)
                sys.exit()
            elif o == "-c":
                config.setConfigPath(a)

            # TODO -v 参数打印log信息
    except getopt.GetoptError:
        Log.error("参数错误")

    config.updateConfig()

    server = Server(wfhelper)
    serverThread = threading.Thread(target=server.startServer)
    serverThread.setDaemon(True)
    serverThread.start()

    # 不用子线程启动的原因是，子线程莫名的速度慢很多
    wfhelper.start()
    