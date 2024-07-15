import time
import neopixel
from board import NEOPIXEL

class Spinner:
    def __init__(self, num_leds=4, color=(55,200,230), dim_by=50) -> None:
        self.num_leds = num_leds
        self.color = color
        self.dim_by = dim_by
        self.pos = 0
        self.leds = neopixel.NeoPixel(NEOPIXEL, num_leds, brightness=0.4, auto_write=False)

    def animate(self, sleep_value=0.12):
        self.leds[self.pos] = self.color
        self.leds[:] = [[max(i - self.dim_by, 0) for i in l] for l in self.leds]
        self.pos = (self.pos+1) % self.num_leds
        self.leds.show()
        time.sleep(sleep_value)
