# type: ignore
from board import *
import touchio
import storage
import neopixel
import usb_midi
import usb_cdc
import usb_hid

pixels = neopixel.NeoPixel(NEOPIXEL, 4)

status = False
trigger = touchio.TouchIn(TOUCH1)
trigger.threshold = 3000

status = trigger.value
dev_name = "RubberDucky"

# testing stuff ---------------
# rval = trigger.raw_value
# tval = trigger.threshold

# print(rval)
# print(tval)
# -----------------------------

if(status == True):
    # Programming mode
    pixels.fill(0xff00ff)
    storage.enable_usb_drive()
    storage.remount("/", readonly=False)
    m = storage.getmount("/")
    m.label = dev_name
    storage.remount("/", readonly=True)
    print("USB drive enabled. RO = True")
else:
    # Execute mode
    pixels.fill(0x000000)
    storage.disable_usb_drive()
    storage.remount("/", readonly=False)
    print("USB drive disabled. RO = False")
    usb_cdc.disable()
    usb_midi.disable()
    usb_hid.enable((Device.KEYBOARD), 0)
    usb_hid.set_interface_name("justakbd")
