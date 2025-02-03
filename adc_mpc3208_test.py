from machine import Pin, SPI
from utime import sleep
from math import atan2, pi, degrees, trunc
# This is actually the first test of my DIY 3d printed high precision hall based rotary sensor
# (see https://www.instagram.com/reel/DFBf_x9ojaP/)
# with micropython and the raspberry pi pico in combination with the mcp3208 adc.

# I connected the two analog signal wires (yellow and blue in the video) to
# the channel 0 and 1. Then the atan2 calculates the angle from the two 90° phase
# shifted sinusoidal signals.

# The concept of the calculation and the sensor design is based on endless potentiometers
# More info on endless potentiometers here: https://github.com/justaboutdone/endless-pots


# MCP Implementation based on https://gist.github.com/SealtielFreak/f69e2c3cb3b1943c2a54f5cf4084f7c8
# but refactored/fixed(?) to work with the MCP3208 which is a 12-bit ADC
class MCP:
    def reference_voltage(self) -> float:
        """Returns the MCP3xxx's reference voltage as a float."""

        raise NotImplementedError

    def read(self, pin: int | None = None, is_differential=False) -> int:
        """
        read a voltage or voltage difference using the MCP3102.
        Args:
            pin: the pin to use
            is_differential: if true, return the potential difference between two pins,
        Returns:
            voltage in range VREF
        """

        raise NotImplementedError


class MCPSerialInterface(MCP):
    def __init__(self, spi, cs, ref_voltage=3.3):
        """
        Create MCP SPI instance
        Args:
            spi: configured SPI bus
            cs:  pin to use for chip select
            ref_voltage: r
        """
        self.cs = cs
        self.cs.value(1)
        self._spi = spi
        self._out_buf = bytearray(3)
        self._in_buf = bytearray(3)
        self._ref_voltage = ref_voltage

    def reference_voltage(self) -> float:
        return self._ref_voltage
    
    @property
    def buffers(self):
        return self._out_buf, self._in_buf


class MCP3208(MCPSerialInterface):
    def read(self, pin=None, is_differential=False):
        if pin == None:
            raise ValueError('Pin must be an int between 0 and 8 representing the channel')
        self.cs.value(0)
        
        # Prepare Output Buffer
        # First Byte needs to end with ... | start bit | is_differential | D2
        self._out_buf[0] = 0x01 << 2 # shift start bit to third position
        self._out_buf[0] = self._out_buf[0] | ((not is_differential) << 1) # merge is_diff on second position
        self._out_buf[0] = self._out_buf[0] | (pin >> 2) # merge the most significant bit of pin on the first position
        # Second Byte needs to begin with | D1 | D2 |... 
        self._out_buf[1] =  (pin & 0b11) << 6 # get only the 2 least significant bits of pin and move the remaining two bits to the most significant position

        self._spi.write_readinto(self._out_buf, self._in_buf)
        self.cs.value(1)

        return ((self._in_buf[1] & 0x0F) << 8) | self._in_buf[2]


pin = Pin("LED", Pin.OUT)
print("LED starts flashing...")
pin_spi0_sck = Pin(2)
pin_spi0_tx = Pin(3)
pin_spi0_rx = Pin(4)
pin_spi_cs = Pin(5, mode=Pin.OUT, value=1)
spi = SPI(0, sck=pin_spi0_sck, mosi=pin_spi0_tx, miso=pin_spi0_rx, baudrate=400000) # for Raspberry Pi Pico

mcp = MCP3208(spi, pin_spi_cs)

maxX = 0
maxY = 0
minX = 9999 # any number above 4095 (= max of 12-bit)
minY = 9999 # any number above 4095 (= max of 12-bit)

while True:
    try:
        pin.toggle()
        valX = mcp.read(0)
        valY = mcp.read(1)

        # auto calibrate
        # TODO: we could save these calibration values eg on the flash storage
        # so that we have good values alread from the start of the pico
        minX = valX if valX < minX else minX
        minY = valY if valY < minY else minY
        maxX = valX if valX > maxX else maxX
        maxY = valY if valY > maxY else maxY
        # normalize
        normX = valX - minX - (maxX -minX)/2
        normY = valY - minY - (maxY -minY)/2
        # get angle
        angle = atan2(normY, normX)
        angle_deg = degrees(angle) + 180
        angle_deg_round = trunc(angle_deg)

        print(f" Angle: {angle_deg_round}; Raw: {valX}, {valY}; Min: {minX}, {minY}; Max: {maxX}, {maxY} Norm: {normX}, {normY}")
        sleep(0.1)
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")