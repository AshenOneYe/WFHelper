import os
import random
import sys

from ppadb.client import Client as AdbClient
from utils.LogUtil import Log


class ADBUtil:

    device = None
    adb = None

    def getScreen(self, savePath=None):
        binary_screenshot = None

        if self.device is not None:
            binary_screenshot = self.device.screencap()

        if savePath is not None and len(binary_screenshot) != 0 and binary_screenshot is not None:
            dirs = os.path.dirname(savePath)

            if not os.path.exists(dirs):
                os.makedirs(dirs)

            with open(savePath, "wb") as f:
                f.write(binary_screenshot)

        return binary_screenshot

    def touchScreen(self, area):
        if self.device is not None:
            self.device.input_tap(
                random.randrange(area[0], area[2]),
                random.randrange(area[1], area[3])
            )

    def swipeScreen(self, x1, y1, x2, y2):
        if self.device is not None:
            self.device.input_swipe(x1, y1, x2, y2, random.uniform(0.5, 1.0))

    def setDevice(self, serial):
        # 用户没有指定设备
        if serial is None:
            devices = self.adb.devices()
            if len(devices) == 0:
                Log.error("未检测到设备连接")
                serial = "127.0.0.1:5555"
                serial = input("请输入设备IP和端口进行连接，默认127.0.0.1:5555\n")
                ip, port = serial.split(":")
                self.adb.remote_connect(str(ip), int(port))
            else:
                Log.info("检测到已连接的设备，请输入序号指定要连接的设备:")
                for i in range(0, len(devices)):
                    print("[{}] - {}".format(i, devices[i].serial))
                try:
                    print("[-1] - 手动输入设备ip和端口进行连接")
                    index = int(input())
                    if index == -1:
                        serial = "127.0.0.1:5555"
                        serial = input("请输入设备IP和端口进行连接，默认127.0.0.1:5555\n")
                        ip, port = serial.split(":")
                        self.adb.remote_connect(str(ip), int(port))
                    else:
                        serial = devices[index].serial
                except ValueError:
                    Log.error("请输入正确的序号!!!")
                    sys.exit()
        self.device = self.adb.device(serial)
        Log.info("设备serial : {}".format(self.device.serial))
        try:
            props = self.device.get_properties()
            Log.info("设备名称 : {}".format(props["ro.product.bootimage.device"]))
            Log.info("制造商 : {}".format(props["ro.product.bootimage.manufacturer"]))
            Log.info("model : {}".format(props["ro.product.bootimage.model"]))
            Log.info("CPU : {}".format(props["ro.product.cpu.abi"]))
            Log.info("系统版本 : {}".format(props["ro.product.build.version.release"]))
        except ValueError:
            Log.error("获取设备信息失败")
            sys.exit()

    def __init__(self):
        if getattr(sys, "frozen", None):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)
        adbPath = os.path.join(basedir, "") + r"adb;"
        os.environ['PATH'] = adbPath + os.environ['PATH']
        os.system("adb start-server")
        self.adb = AdbClient(host="127.0.0.1", port=5037)


adbUtil = ADBUtil()
