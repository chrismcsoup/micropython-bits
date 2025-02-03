# Demo with raspberry pi pico w (rp2040) with micropython
# of the rotary encoder KY-040
# bought on Amazon.de https://amzn.eu/d/5MI3Yel

# Using the library from miketeachman (https://github.com/miketeachman/micropython-rotary)

# For usage with a mcp230xx Port Expander have a look at the following Pull Request:
# https://github.com/miketeachman/micropython-rotary/pull/36/files

# When the rotary encoder is pressed then the state is printed and the pico's internal
# led is switched on. On release the led is turned of.
# On rotating the rotary encoder the numerical value is printed in the console.

from time import sleep
from rotary_irq_rp2 import RotaryIRQ
from machine import Pin

# The Pins
# + --> 3V3(OUT) on PICO because we are acting on a digital logic level
# GND --> GND on PICO
pin_nr_gpio_switch = 18 # SW on Rotary Encoder
pin_nr_gpio_clk = 17 # CLK on Rotary Encoder
pin_nr_gpio_dt = 16 # DT on Rotary Encoder

led = Pin("LED", Pin.OUT)
button = Pin(pin_nr_gpio_switch, Pin.IN)

r = RotaryIRQ(pin_num_clk=pin_nr_gpio_clk, 
              pin_num_dt=pin_nr_gpio_dt, 
              min_val=0, 
              max_val=5, 
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_UNBOUNDED)
              
val_old = r.value()

def callback():
    print(f'result = {r.value()}')

# add a callback function that is called on each movement of the encoder
r.add_listener(callback)

# When the button is pressed the value is 0 (NOT 1)
old_button_val = 1
while True:
    new_button_val = button.value()
    if new_button_val != old_button_val:
        print(f'Button State: {new_button_val}')
        if new_button_val == 0:
            led.on()
        else:
            led.off()
    old_button_val = new_button_val
    sleep(0.05)
