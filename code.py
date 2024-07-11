# type: ignore
import time
import usb_hid
import supervisor
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_de import KeyboardLayout
from statuslight import Spinner
import di as ducky
from touchio import TouchIn
from board import TOUCH1


switch_pin = TouchIn(TOUCH1)
switch_pin.threshold = 3000


time.sleep(1)
supervisor.runtime.autoreload = False

if switch_pin.value:
    my_color = (160,235,255)

    spinner = Spinner(color=my_color)
    while True:
        try:
            spinner.animate()
        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
            break
else:
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayout(kbd)

    duck = ducky.Ducky('payload.dd', kbd, layout)

    result = True
    while result is not False:
        result = duck.runScript()
