"""Provides a class to run Ducky-like script.

Returns:
    object: Instance of a Ducky-class object

**Quickstart: Importing and using the class**

    First, importing libraries
    
    ```py
    import time
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keyboard_layout import KeyboardLayout
    import ducky
    ```
    
    Next, define the keyboard layout and initialze the `Ducky` class.
    
    ```py
    time.sleep(1)
    keyboard = Keyboard(usb_hid.devices)
    layout = KeyboardLayout(keyboard)

    duck = ducky.Ducky('payload.dd', keyboard, layout) # you will additionally need a commands dict
    ```
    
    Now you can run `runScript()` in a loop, which will execute the script line by line.
    
    ```py
    status = True
    while status is not False:
        status = duck.runScript()
    ```
"""

# imports
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_base import KeyboardLayoutBase

class Ducky:
    """Class that runs a Ducky-like script file.
    """


    def __init__(self, filename: str, keyboard: Keyboard, layout: KeyboardLayoutBase, commands: dict) -> None:
        self.keyboard = keyboard
        self.layout = layout
        self.commands = commands
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
        """Writes keys over HID. Also used with more complicated commands.

        Args:
            key (str): The string or command which to write
        """
        if key in self.commands:
            self.keyboard.press(self.commands[key])
        else:
            self.layout.write(key)


    def runScript(self) -> bool:
        """Function that sends a line of provided script file over HID every time it is called.

        Returns:
            bool: False once the script has no more lines and ends.
        """

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
