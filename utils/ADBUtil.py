import os
import random
import sys
import adbutils

from utils.ImageUtil import readImageFromBytes
from utils.LogUtil import Log

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)


class ADBUtil:

    device = None
    rplc = b"\r\n"
    test = False
    lastScreenBytes = None

    def getScreen(self, savePath=None):

        cmd = "screencap -p"

        stream = self.device.shell(cmd, stream=True)

        binary_screenshot = b""
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            binary_screenshot += chunk

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
        self.device.click(
            random.randrange(area[0], area[2]),
            random.randrange(area[1], area[3])
        )

    def setDevice(self, serial):
        # 用户没有指定设备
        if serial is None:
            devices = adb.device_list()
            if len(devices) == 0:
                Log.error("未检测到设备连接")
                serial = "127.0.0.1:5555"
                serial = input("请输入设备IP和端口进行连接，默认127.0.0.1:5555\n")
                out = adb.connect(serial, timeout=3)
                Log.info(out)
            elif len(devices) == 1:
                serial = devices[0]._serial
                Log.info("只检测到一台设备，默认与其建立连接")
            else:
                Log.info("发现多台设备，请输入序号指定要连接的设备:")
                for i in range(0, len(devices)):
                    print("{} - {}".format(i, devices[i]._serial))
                try:
                    serial = devices[int(input())]._serial
                except ValueError:
                    Log.error("请输入正确的序号!!!")
                    sys.exit()
        self.device = adbutils.AdbDevice(adb, serial=serial)
        adb.connect(self.device._serial, 3)
        Log.info("设备serial : {}".format(self.device._serial))
        try:
            Log.info("设备信息 : {}".format(self.device.prop))
        except adbutils.errors.AdbError:
            Log.error("获取设备信息失败")
            sys.exit()


adbUtil = ADBUtil()
