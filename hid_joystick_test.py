from micropython import const
import time
import usb.device
from usb.device.hid import HIDInterface
from machine import Pin

pin = Pin("LED", Pin.OUT)
print("LED starts flashing...")

_INTERFACE_PROTOCOL_JOYSTICK = const(0x00)  # Generic joystick protocol

def joystick_example():
    j = JoystickInterface()

    # Initialize USB device with the joystick interface
    usb.device.get().init(j, builtin_driver=True)

    # Wait until the interface is open
    while not j.is_open():
        pin.toggle()
        time.sleep_ms(100)

    pin.on()
    # Main loop: simulate joystick movement
    while True:
        print("Joystick: Center")
        j.send_joystick(0, 0)  # Center position
        time.sleep(1)

        print("Joystick: Top-Left")
        j.send_joystick(-127, -127)  # Top-left
        time.sleep(1)

        print("Joystick: Bottom-Right")
        j.send_joystick(127, 127)  # Bottom-right
        time.sleep(1)

        print("Joystick: Starting again...")


class JoystickInterface(HIDInterface):
    # Basic USB joystick HID interface

    def __init__(self):
        super().__init__(
            _JOYSTICK_REPORT_DESC,
            set_report_buf=bytearray(2),  # X and Y axes
            protocol=_INTERFACE_PROTOCOL_JOYSTICK,
            interface_str="MicroPython Joystick",
        )

    def send_joystick(self, x, y):
        """Send joystick X and Y axis data."""
        # Convert axis values (-127 to 127) to unsigned bytes (0 to 255)
        x = max(-127, min(127, x)) & 0xFF
        y = max(-127, min(127, y)) & 0xFF
        self.send_report(bytes([x, y]))


# HID Report descriptor for a joystick with 2 axes
#
# fmt: off
_JOYSTICK_REPORT_DESC = (
    b'\x05\x01'        # Usage Page (Generic Desktop)
    b'\x09\x04'        # Usage (Joystick)
    b'\xA1\x01'        # Collection (Application)
        b'\x05\x01'    # Usage Page (Generic Desktop)
        b'\x09\x01'    # Usage (Pointer)
        b'\xA1\x00'    # Collection (Physical)
            b'\x15\x81'  # Logical Minimum (-127)
            b'\x25\x7F'  # Logical Maximum (127)
            b'\x75\x08'  # Report Size (8 bits)
            b'\x95\x02'  # Report Count (2) - X and Y axes
            b'\x09\x30'  # Usage (X)
            b'\x09\x31'  # Usage (Y)
            b'\x81\x02'  # Input (Data, Variable, Absolute)
        b'\xC0'          # End Collection
    b'\xC0'              # End Collection
)
# fmt: on


# Run the joystick example
joystick_example()
