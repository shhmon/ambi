import cv2
import numpy as np
from mss.darwin import MSS as mss
from mss import tools
# from PIL import Image, ImageGrab

# import gi

# gi.require_version("Gdk", "3.0")
# from gi.repository import Gdk as gdk

# NOTE: Works reasonably well for smaller regions
def image_grab_mss(left, top, width, height, debug=False):
    with mss() as sct:
        monitor = {
            "top": top,
            "left": left,
            "width": width,
            "height": height
        }

        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        res = cv2.resize(img, dsize=(int(16), int(10)), interpolation=cv2.INTER_LINEAR)

        if debug:
            output = "scrt-{top}x{left}_{width}x{height}.png".format(**monitor)
            tools.to_png(sct_img.rgb, sct_img.size, output=output)
        
        return res

# NOTE: gdk doesn't seem to work on my machine
def image_grab_gdk(left, top, width, height):
    win = gdk.get_default_root_window()

    s = gdk.pixbuf_get_from_window(win,left,top, width, height)
    
    final = Image.frombuffer(
        "RGB",
        (width, height),
        s.get_pixels(),
        "raw",
        "RGB",
        s.get_rowstride(), 1)
    
    return final

# NOTE: This is too slow
def image_grab_pygetwindow(left, top, right, bot):
    bbox = (left, top, right, bot)
    img = ImageGrab.grab(bbox)
    return img