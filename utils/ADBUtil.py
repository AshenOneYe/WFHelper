import os
import random
import sys

from ppadb.client import Client as AdbClient
from ppadb.device import Device
from .LogUtil import Log


def getADB():
    if getattr(sys, "frozen", None):
        basedir = getattr(sys, "_MEIPASS")
    else:
        basedir = os.path.dirname(__file__)
    adbPath = os.path.join(basedir, "") + r"adb;"
    os.environ['PATH'] = adbPath + os.environ['PATH']
    os.system("adb start-server")
    adb = AdbClient(host="127.0.0.1", port=5037)
    return adb


def getScreen(device: Device, savePath=None):
    currentframe = None

    if device is not None:
        currentframe = device.screencap()

    if savePath is not None and currentframe is not None:
        dirs = os.path.dirname(savePath)

        if not dirs == "" and not os.path.exists(dirs):
            os.makedirs(dirs)

        with open(savePath, "wb") as f:
            f.write(currentframe)

    return currentframe


def touchScreen(device: Device, area):
    if device is None:
        raise Exception
    device.input_tap(
        random.randrange(round(float(area[0])), round(float(area[2]))),
        random.randrange(round(float(area[1])), round(float(area[3])))
    )


def swipeScreen(device: Device, x1, y1, x2, y2):
    if device is None:
        raise Exception
    device.input_swipe(x1, y1, x2, y2, int(random.uniform(0.5, 1.0) * 1000))


def selectSerial():
    adb = getADB()
    devices = adb.devices()
    if len(devices) == 0:
        print("未检测到设备连接")
        serial = "127.0.0.1:5555"
        serial = input("请输入设备IP和端口进行连接，默认127.0.0.1:5555\n")
        ip, port = serial.split(":")
        adb.remote_connect(str(ip), int(port))
    else:
        print("检测到已连接的设备，请输入序号指定要连接的设备:")
        for i in range(0, len(devices)):
            print("[{}] - {}".format(i, devices[i].serial))
        try:
            print("[-1] - 手动输入设备ip和端口进行连接")

            index = input()
            if index is None or index == "":
                index = 0
            else:
                index = int(index)

            if index == -1:
                serial = "127.0.0.1:5555"
                serial = input("请输入设备IP和端口进行连接，默认127.0.0.1:5555\n")
                ip, port = serial.split(":")
                adb.remote_connect(str(ip), int(port))
            else:
                serial = devices[index].serial
        except ValueError:
            Log.error("请输入正确的序号!!!")
    return serial


def getDevice(serial):
    # 用户没有指定设备
    if serial is None:
        return
    adb = getADB()
    device = adb.device(serial)
    return device


def logDeviceInfo(device: Device):
    try:
        Log.info(f"设备serial : {device.serial}")
        props = device.get_properties()
        Log.info("设备名称 : {}".format(props["ro.product.device"]))
        Log.info("制造商 : {}".format(props["ro.product.manufacturer"]))
        Log.info("model : {}".format(props["ro.product.model"]))
        Log.info("CPU : {}".format(props["ro.product.cpu.abi"]))
        Log.info("系统版本 : {}".format(props["ro.build.version.release"]))
        size = device.wm_size()
        Log.info("分辨率 : {}x{}".format(size[1], size[0]))
    except ValueError:
        Log.error("获取设备信息失败")
