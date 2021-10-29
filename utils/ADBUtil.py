import subprocess
import os
import random


class ADBUtil():

    device = None

    def getScreen(self,savePath=None):

        cmd = "adb " 

        if self.device != None:
            cmd += "-s {} ".format(self.device)

        cmd += "shell screencap -p"

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        
        binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
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
            

