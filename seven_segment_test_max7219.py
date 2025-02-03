# Demo with raspberry pi pico w (rp2040) with micropython
# of the red 8x 7-segment display based on MAX7219 from
# AZ_Delivery https://www.az-delivery.de/en/products/azdelivery-max7219-led-modul-8-bit-7-segmentanzeige-led-display-fur-arduino-und-raspberry-pi
# bought on Amazon.de https://www.amazon.de/dp/B07Z7RLGC2

# Library used from PaulDash (https://github.com/PaulDash/micropython-max7219)
# which is based/forked from JennaSys but extend to be compatible with pi pico
from machine import Pin, SPI  # type: ignore
from time import sleep
from max7219 import SevenSegment

# The Pins
# VCC --> VBUS on PICO (= +5V USB) 
# GND --> GND on PICO
pin_spi0_sck = Pin(2) # = CLK on 7-Segment Module
pin_spi0_tx = Pin(3) # = DIN on 7-Segment Module
pin_gpio_cs = Pin(15) # = CS n 7-Segment Module

display = SevenSegment(digits=8, scan_digits=8, pin_cs=pin_gpio_cs, pin_clk=pin_spi0_sck, pin_din=pin_spi0_tx, spi_bus=0, reverse=True)
display.brightness(0) # 0..15
display.text("ABCDEF")
sleep(5)
display.number(3.14159)
display.brightness(8) # 0..15
sleep(5)
display.brightness(15) # 0..15
display.message("Hello World")
sleep(5)
display.clear()