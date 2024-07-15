<h1 align="center">sneaky-ducky</h1>

<div align="center">
    <strong>Create a stealthy budget USB Rubber Ducky</strong>
</div>

<br />

<div align="center">
    <img alt="GitHub License" src="https://img.shields.io/github/license/6ooker/sneaky-ducky">
    <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/6ooker/sneaky-ducky">

</div>


<br />

## Introduction

Library for the SAMD21-based Adafruit NeoTrinkey M0 as a covert USB Rubber Ducky implementation.

## Dependencies


-----

# Hardware Instructions

# Software Instructions

Follow these steps:

1. Download the latest release from the [Releases](https://github.com/6ooker/sneaky-ducky) page or clone the repo to get a local copy of the files. `git clone https://github.com/6ooker/sneaky-ducky.git`

2. Download [CircuitPython for the NeoPixel Trinkey M0](https://circuitpython.org/board/neopixel_trinkey_m0/) *Tested v9.0.5

3. Plug the Neo Trinkey into a USB port and double click the small reset button. It will show up as a storage device called `TRINKEYBOOT`.

4. Copy the downloaded `.uf2` file to the root folder of `TRINKEYBOOT`. The device will reboot and a new disk drive called `CIRCUITPY` will appear.

5. Copy the `lib` folder to the root of your device.

6. Copy `*.py` to the root of your Trinkey.

7. Follow the instructions to enter setup mode.

8. Save your script file as `payload.dd` on your Trinkey and you're ready to go.

## Setup mode

In order to see the device as a storage device and save payloads as well as not inject your own machine you will have to blah blah to enter setup mode.
bild

## Changing Keyboard Layouts

Visit [the Neradoc's library](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts) for additional layouts.

For supported languages get the `keyboard-layouts-9.x-mpy.zip` version from the [Releases](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/releases/latest) page.

This project uses the `.mpy` version due to the limited memory available on SAMD21 based boards.

### Code adjustments

At the start of `commands.py` and `code.py` comment out these lines:

```py
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
```

And uncomment these lines (*replace `LANG` with your desired language*):

```py
from keyboard_layout_win_LANG import KeyboardLayout
from keycode_win_LANG import Keycode
```

## Useful links and resources

### Docs

[CircuitPython](https://docs.circuitpython.org/en/9.0.x/README.html)

[CircuitPython HID](https://learn.adafruit.com/circuitpython-essentials/circuitpython-hid-keyboard-and-mouse)

## Related Projects

## Credits
