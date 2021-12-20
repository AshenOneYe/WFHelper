import scrcpy
from PIL import Image
from ImageUtil import img2bytes

client = scrcpy.Client(device="192.168.137.164:5555")


def on_frame(frame):

    # If you set non-blocking (default) in constructor, the frame event receiver
    # may receive None to avoid blocking event.
    if frame is not None:
        # frame is an bgr numpy ndarray (cv2' default format)
        img = Image.fromarray(frame)
        open("test.png", "wb").write(img2bytes(img))
        exit()


client.add_listener(scrcpy.EVENT_FRAME, on_frame)
client.start()
