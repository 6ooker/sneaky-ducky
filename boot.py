# type: ignore
from board import NEOPIXEL, TOUCH1
import touchio
import storage
import neopixel
import usb_midi
import usb_cdc
import usb_hid

pixels = neopixel.NeoPixel(NEOPIXEL, 4)

programmingStatus = False
programmingPin = touchio.TouchIn(TOUCH1)   # we are using TOUCH1 (CP Name from board) as the programming pin
programmingPin.threshold = 3000            # threshold needs to be manually set to ~3000 to not get false-positive readings
programmingStatus = programmingPin.value

dev_name = "RubberDucky" # just the name for the data drive the board will be visible as

if(programmingStatus == True):
    # Programming mode
    pixels.fill(0xff00ff)
    storage.enable_usb_drive()                  # show up as a USB mass storage device
    storage.remount("/", readonly=False)
    m = storage.getmount("/")
    m.label = dev_name
    storage.remount("/", readonly=True)         # Readonly is from CPs POV, not host computer
    print("USB drive enabled. RO = True")
else:
    # Execute mode
    pixels.fill(0x000000)
    storage.disable_usb_drive()                 # don't present a USB mass storage device
    storage.remount("/", readonly=False)
    print("USB drive disabled. RO = False")
    usb_cdc.disable()                           # disable cdc
    usb_midi.disable()                          # and midi so the device won't show up as such when in exec mode
    usb_hid.enable((Device.KEYBOARD), 0)
    usb_hid.set_interface_name("justakbd")
