# type: ignore
from board import *
import supervisor
import time
from statuslight import Spinner
import touchio

time.sleep(.5)
supervisor.runtime.autoreload = False
touch = touchio.TouchIn(TOUCH1)
touch.threshold = 3000

if not touch.value:
    from duckyinterpreter import main_loop
    main_loop()
    time.sleep(1)

my_color = (160,235,255)

spinner = Spinner(color=my_color)

while True:
    try:
        spinner.animate()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        # pixels.fill(0x000000)
        break
