# Demo with raspberry pi pico w (rp2040) with micropython
# of the red 8x32 Dot Matrix LED based on MAX7219 from
# AZ_Delivery https://www.az-delivery.de/en/products/4-x-64er-led-matrix-display
# bought on Amazon.de https://amzn.eu/d/am4Ig8N

# Using the library from mcauser (https://github.com/mcauser/micropython-max7219)

from led_matrix_max7219 import Matrix8x8
from machine import Pin, SPI
from time import sleep


# The Pins
# VCC --> VBUS on PICO (= +5V USB) 
# GND --> GND on PICO
pin_spi0_sck = Pin(2) # = CLK on Led Matrix
pin_spi0_tx = Pin(3) # = DIN on Led Matrix
pin_gpio_cs = Pin(15) # = CS on Led Matrix


spi = SPI(0, baudrate=14500000, sck=pin_spi0_sck, mosi=pin_spi0_tx) 

display = Matrix8x8(spi, pin_gpio_cs, 4)
display.brightness(0)
display.text('1234',0,0,1)
display.show()
sleep(5)
display.fill(0)
display.brightness(15)
display.text('5678',0,0,1)
display.show()
sleep(5)
display.fill(0)
display.show()