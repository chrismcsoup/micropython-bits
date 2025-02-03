from machine import Pin
from utime import sleep
from neopixel import NeoPixel

pin = Pin("LED", Pin.OUT)
neo_pin= Pin(6, Pin.OUT)   # set GPIO6 to output to drive NeoPixels
np = NeoPixel(neo_pin, 64)   # create NeoPixel driver on GPIO0 for 8 pixels
print("LED starts flashing...")

counter = 0
counter_limit = 250
while True:
    try:
        pin.toggle()
        if counter % 10 == 0:
            np[1] = (counter, counter, counter) # type: ignore # set the first pixel to white
        else:
            np[1] = (0, 0, 0) # type: ignore # set the first pixel to white
        np.write()              # write data to all pixels
        if counter >= counter_limit:
            counter = 0
        else:
            counter += 5
        r, g, b = np[1]         # type: ignore # get first pixel colour
        print(f'pixel color:{r},{g},{b}')
        sleep(1)
    except KeyboardInterrupt:
        break
pin.off()
np[1] = (0, 0, 0) # type: ignore
np.write()
print("Finished.")