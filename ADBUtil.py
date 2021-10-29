import subprocess
import os

def getScreen(filename=None):
    cmd = "adb shell screencap -p"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    binary_screenshot = process.stdout.read()
    
    binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
    if filename != None:
        with open(filename,'wb') as f:
            f.write(binary_screenshot)
    return binary_screenshot

def touchScreen(pos):
    cmd = "adb shell input tap {} {}".format(pos[0],pos[1])
    os.system(cmd)
    

