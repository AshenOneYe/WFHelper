import subprocess
import os
import random
import sys
from utils.LogUtil import Log
from utils.ImageUtil import readImageFromBytes


class ADBUtil():

    device = None
    rplc = b'\r\n'
    test = False
    lastScreenBytes = None

    def getDeviceList(self):
        cmd = "adb devices"
        process = os.popen(cmd)
        devices = process.readlines()
        try:
            devices = devices[1:len(devices)-1]
        except:       
            Log.error("获取设备列表失败")
        return devices

    def getScreen(self,savePath=None):

        cmd = "adb " 

        if self.device != None:
            cmd += "-s {} ".format(self.device)

        cmd += "shell screencap -p"

        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        
        if not self.test:
            try:  
                readImageFromBytes(binary_screenshot.replace(self.rplc, b'\n'))
            except Exception:
                self.rplc = b'\r\r\n'
            finally:
                self.test = True

        binary_screenshot = binary_screenshot.replace(self.rplc, b'\n')
        if savePath != None and len(binary_screenshot) != 0:
            with open(savePath,'wb') as f:
                f.write(binary_screenshot)

        self.lastScreenBytes = binary_screenshot
        return binary_screenshot


    def touchScreen(self,area):   
        cmd = "adb "

        if self.device != None:
            cmd += "-s {} ".format(self.device)

        cmd += "shell input tap {} {}".format(random.randrange(area[0],area[2]),random.randrange(area[1],area[3]))

        os.system(cmd)

    def setDevice(self,device):
        if device == None:
            devices = self.getDeviceList()
            if len(devices) == 0:
                Log.error("未检测到设备连接")
            if len(devices) == 1:
                device = devices[0].split("\t")[0]
                Log.info("只检测到一台设备，默认与其建立连接")
            else:
                Log.info("发现多台设备，请输入序号指定要连接的设备:")
                for i in range(0,len(devices)):
                    print("{} : {}".format(i,devices[i]))
                try:
                    device = devices[int(input())]
                except:
                    Log.error("请输入正确的序号!!!")
                    sys.exit()
        if device == None:
            sys.exit()
        self.device = device
        Log.info("设备名 : {}".format(self.device))

adbUtil = ADBUtil()