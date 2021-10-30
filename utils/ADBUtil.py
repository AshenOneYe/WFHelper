import subprocess
import os
import random
from utils.ImageUtil import readImageFromBytes


class ADBUtil():

    device = None
    rplc = b'\r\n'
    test = False

    def getScreen(self,savePath=None):

        cmd = "adb " 

        if self.device != None:
            cmd += "-s {} ".format(self.device)

        cmd += "shell screencap -p"

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
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
        return binary_screenshot


    def touchScreen(self,area):   
        cmd = "adb "

        if self.device != None:
            cmd += "-s {} ".format(self.device)

        cmd += "shell input tap {} {}".format(random.randrange(area[0],area[2]),random.randrange(area[1],area[3]))

        os.system(cmd)

    def setDevice(self,device):
        self.device = device