"""
`ducky`
==================================================

Library for interpreting and running Ducky-like script files

* Author(s): Erik Katzenberger

Implementation Notes
--------------------

**Software and Dependencies**

* Adafruit CircutPython firmware for supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from adafruit_hid.keyboard import Keyboard
import time

# from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
# from adafruit_hid.keycode import Keycode

from keyboard_layout_win_de import KeyboardLayout
from keycode_win_de import Keycode

__version__ = "0.0.0+auto.0"
__repo__ = "<repo>"

commands = {
    'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI, 'WIN': Keycode.WINDOWS,
    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
    'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
    'BACKSPACE': Keycode.BACKSPACE,
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
    'F12': Keycode.F12,

}

class Ducky:
    """
    Class that runs a Ducky-like script file.

    **Quickstart: Importing and using the library**

        An example of using the :class:`Ducky` class.
        First, import the libraries

            .. code-block:: python

            import time
            import usb_hid
            from adafruit_hid.keyboard import Keyboard
            from adafruit_hid.keyboard_layout import KeyboardLayout
            import ducky

        Once done, define the keyboard layout and initialize the :class:`Ducky` class.

            .. code-block:: python

            time.sleep(1)
            keyboard = Keyboard(usb_hid.devices)
            layout = KeyboardLayout(keyboard)

            duck = ducky.Ducky('payload.dd', keyboard, layout)

        Now you can run a loop to run the script line by line, per each iteration, via `runScript`.

            .. code-block:: python

            status = True
            while status is not False:
                status = duck.runScript()

    """


    def __init__(self, filename: str, keyboard: Keyboard, layout: KeyboardLayout) -> None:
        self.keyboard = keyboard
        self.layout = layout
        self.lines = []
        self.default_delay = 0.0
        self.prev_line = None
        self.next_index = 0
        self.wait = 0.0
        self.repeat = 0

        with open(filename, "r", encoding='utf-8') as duckyscript:
            for line in duckyscript:
                line = line.lstrip(" ").rstrip("\n\r")
                if len(line) > 0:
                    self.lines.append(line)


    def write_key(self, key: str) -> None:
        """Writes keys over HID. Also used with more complicated commands."""
        if key in commands:
            self.keyboard.press(commands[key])
        else:
            self.layout.write(key)


    def runScript(self) -> bool:
        """Function that sends a line of provided script file over HID every time it is called."""

        now = time.monotonic()
        if now < self.wait:
            return True

        try:
            if self.repeat > 0:
                self.repeat -= 1
                line = self.prev_line
            else:
                line = self.lines[self.next_index]
                self.next_index += 1
        except IndexError:
            print("  DONE!")
            self.prev_line = None
            self.next_index = 0
            return False

        words = line.split(" ", 1)
        command = words[0]

        if command == "REPEAT":
            self.repeat = int(words[1])
            # time.sleep(float(self.default_delay)/1000)
            return True

        self.prev_line = line

        if command == "REM":
            return True

        self.wait = now + self.default_delay

        if command in ("DEFAULT_DELAY", "DEFAULTDELAY"):
            self.wait -= self.default_delay
            self.default_delay = float(words[1])/1000
            self.wait += self.default_delay
            return True

        if command == "DELAY":
            self.wait += float(words[1])/1000
            return True

        if command == "STRING":
            self.layout.write(words[1])
            return True

        self.write_key(command)
        if len(words) > 1:
            for key in filter(None, words[1].split(" ")):
                self.write_key(key)

        self.keyboard.release_all()
        return True
