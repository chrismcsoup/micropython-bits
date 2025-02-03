from machine import Pin, I2C
from sh1106 import SH1106_I2C
from time import sleep

# A test with raspberry pi pico w (rp2040) with the 
# 1.3" white oled display with SH1106 driver from AZ-Delivery 
# https://www.az-delivery.de/en/products/1-3zoll-i2c-oled-display

# Using the SH1106 library from robert-hh (https://github.com/robert-hh/SH1106)


def color565(r, g, b):
    """Return RGB565 color value.

    Args:
        r (int): Red value.
        g (int): Green value.
        b (int): Blue value.
    """
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height

# The Pins
# VCC --> VBUS on PICO (= +5V USB) 
# GND --> GND on PICO
pin_i2c0_scl = Pin(1) # SCK on Display Module
pin_i2c0_sda = Pin(0) # SDA on Display Module

i2c = I2C(0, scl=pin_i2c0_scl, sda=pin_i2c0_sda)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config

# set the addr to the I2C Address of the device (0X3C as default)
display = SH1106_I2C(WIDTH, HEIGHT, i2c, res=None, addr=0X3C, rotate=0, delay=0)
display.init_display()
display.poweron()
display.fill(0)
display.text('Testing 1', 10, 30, 1)
display.rect(0,0,WIDTH,HEIGHT,color565(255,255,255))
display.contrast(255)
display.show()
sleep(5)
display.poweroff()