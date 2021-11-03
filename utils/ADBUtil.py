import os
import random
import subprocess
import sys

from utils.ImageUtil import readImageFromBytes
from utils.LogUtil import Log


class ADBUtil:

    device = None
    rplc = b"\r\n"
    test = False
    lastScreenBytes = None

    # 解决打包前打包后路径不一致问题https://cloud.tencent.com/developer/article/1739886
    def base_path(self, path):
        if getattr(sys, "frozen", None):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)
        return os.path.join(basedir, path)

    def getDeviceList(self):
        cmd = self.base_path("") + r"adb\adb.exe devices"
        process = os.popen(cmd)
        devices = process.readlines()
        try:
            devices = devices[1 : len(devices) - 1]
        except:
            Log.error("获取设备列表失败")
        return devices

    def getScreen(self, savePath=None):

        cmd = self.base_path("") + r"adb\adb.exe "

        if self.device is not None:
            cmd += "-s {} ".format(self.device)

        cmd += "shell screencap -p"

        process = subprocess.Popen(
            cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        binary_screenshot = process.stdout.read()

        if not self.test:
            try:
                readImageFromBytes(binary_screenshot.replace(self.rplc, b"\n"))
            except Exception:
                self.rplc = b"\r\r\n"
            finally:
                self.test = True

        binary_screenshot = binary_screenshot.replace(self.rplc, b"\n")
        if savePath is not None and len(binary_screenshot) != 0:
            with open(savePath, "wb") as f:
                f.write(binary_screenshot)

        self.lastScreenBytes = binary_screenshot
        return binary_screenshot

    def touchScreen(self, area):
        cmd = self.base_path("") + r"adb\adb.exe "

        if self.device is not None:
            cmd += "-s {} ".format(self.device)

        cmd += "shell input tap {} {}".format(
            random.randrange(area[0], area[2]), random.randrange(area[1], area[3])
        )

        os.system(cmd)

    def setDevice(self, device):
        if device is None:
            devices = self.getDeviceList()
            if len(devices) == 0:
                Log.error("未检测到设备连接")
            if len(devices) == 1:
                device = devices[0].split("\t")[0]
                Log.info("只检测到一台设备，默认与其建立连接")
            else:
                Log.info("发现多台设备，请输入序号指定要连接的设备:")
                for i in range(0, len(devices)):
                    print("{} : {}".format(i, devices[i]))
                try:
                    device = devices[int(input())]
                except:
                    Log.error("请输入正确的序号!!!")
                    sys.exit()
        if device is None:
            sys.exit()
        self.device = device
        Log.info("设备名 : {}".format(self.device))


adbUtil = ADBUtil()
