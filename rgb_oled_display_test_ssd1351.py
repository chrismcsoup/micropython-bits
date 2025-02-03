"""SSD1351 demo (shapes)."""
from time import sleep
from ssd1351 import Display, color565
from machine import Pin, SPI  # type: ignore


def test():
    """Test code."""
    # Raspberry Pi Pico / Pico W Pin
    # with 1.5" 128x128px RGB Oled Display from Waveshare with a ssd1351 chip
    # (https://www.waveshare.com/1.5inch-rgb-oled-module.htm) 
    # via amazon.de https://amzn.eu/d/3zMXw0i

    # Used the micro python library for SSD1351 from rdagger 
    # (https://github.com/rdagger/micropython-ssd1351)

    # VCC --> VBUS on PICO (= +5V USB) 
    # GND --> GND on PICO

    # The following pins need to be SPI Pins on the Pico
    pin_spi0_sck = Pin(2) # = CLK on Display Module
    pin_spi0_tx = Pin(3) # = DIN on Display Module

    # The following pins can by any GPIO Pins on the Pico
    pin_gpio_cs = Pin(13) # = CS n Display Module
    pin_gpio_dc = Pin(14) # = DC on Display Module
    pin_gpio_rst = Pin(15) # = RST on Display Module
    

    # Baud rate of 14500000 seems about the max
    spi = SPI(0, baudrate=14500000, sck=pin_spi0_sck, mosi=pin_spi0_tx) 
    display = Display(spi, dc=pin_gpio_dc, cs=pin_gpio_cs, rst=pin_gpio_rst)

    display.clear(color565(64, 0, 255))
    sleep(1)

    display.clear()

    display.draw_rectangle(0, 0, 128, 128, color565(255, 255, 255))
    sleep(1)
    display.clear()

    display.draw_hline(10, 127, 63, color565(255, 0, 255))
    sleep(1)

    display.draw_vline(10, 0, 127, color565(0, 255, 255))
    sleep(1)

    display.fill_hrect(23, 50, 30, 75, color565(255, 255, 255))
    sleep(1)

    display.draw_hline(0, 0, 127, color565(255, 0, 0))
    sleep(1)

    display.draw_line(127, 0, 64, 127, color565(255, 255, 0))
    sleep(2)

    display.clear()

    coords = [[0, 63], [78, 80], [122, 92], [50, 50], [78, 15], [0, 63]]
    display.draw_lines(coords, color565(0, 255, 255))
    sleep(1)

    display.clear()
    display.fill_polygon(7, 63, 63, 50, color565(0, 255, 0))
    sleep(1)

    display.fill_rectangle(0, 0, 15, 127, color565(255, 0, 0))
    sleep(1)

    display.clear()

    display.fill_rectangle(0, 0, 63, 63, color565(128, 128, 255))
    sleep(1)

    display.draw_rectangle(0, 64, 63, 63, color565(255, 0, 255))
    sleep(1)

    display.fill_rectangle(64, 0, 63, 63, color565(128, 0, 255))
    sleep(1)

    display.draw_polygon(3, 96, 96, 30, color565(0, 64, 255),
                         rotate=15)
    sleep(3)

    display.clear()

    display.fill_circle(32, 32, 30, color565(0, 255, 0))
    sleep(1)

    display.draw_circle(32, 96, 30, color565(0, 0, 255))
    sleep(1)

    display.fill_ellipse(96, 32, 30, 16, color565(255, 0, 0))
    sleep(1)

    display.draw_ellipse(96, 96, 16, 30, color565(255, 255, 0))

    sleep(5)
    display.cleanup()


test()