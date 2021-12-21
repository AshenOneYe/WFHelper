import scrcpy
from PIL import Image
from ImageUtil import img2bytes
from adbutils import AdbClient


adb = AdbClient()
client = scrcpy.Client(device=adb.device_list()[0])


def on_frame(frame):

    # If you set non-blocking (default) in constructor, the frame event receiver
    # may receive None to avoid blocking event.
    if frame is not None:
        # frame is an bgr numpy ndarray (cv2' default format)
        img = Image.fromarray(frame)
        img2bytes(img)


client.add_listener(scrcpy.EVENT_FRAME, on_frame)
client.start()
