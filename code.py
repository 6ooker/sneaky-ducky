# type: ignore
import time
import usb_hid
import supervisor
from touchio import TouchIn
from board import TOUCH1
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
# from keyboard_layout_win_de import KeyboardLayout
from statuslight import Spinner
import commands
import ducky

switch_pin = TouchIn(TOUCH1)    # we are using TOUCH1 (CP Name from board) as the programming pin
switch_pin.threshold = 3000     # threshold needs to be manually set to ~3000 to not get false-positive readings


time.sleep(1)                           # wait a second to init system
supervisor.runtime.autoreload = False   # we don't want autoreloads

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
    cmds = commands.commands

    duck = ducky.Ducky('payload.dd', kbd, layout, cmds)

    result = True
    while result is not False:
        result = duck.runScript()
