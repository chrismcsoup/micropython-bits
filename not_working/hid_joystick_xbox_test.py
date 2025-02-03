from micropython import const
import time
import usb.device
from usb.device.hid import HIDInterface
from machine import Pin

pin = Pin("LED", Pin.OUT)
print("LED starts flashing...")

_INTERFACE_PROTOCOL_GAMEPAD = const(0x00)  # Generic gamepad protocol

def xbox_controller_example():
    controller = XboxControllerInterface()

    # Initialize USB device with the Xbox controller interface
    usb.device.get().init(controller, builtin_driver=True)

    # Wait until the interface is open
    while not controller.is_open():
        pin.toggle()
        time.sleep_ms(100)

    pin.on()
    # Main loop: simulate Xbox controller movements
    while True:
        print("Controller: Center")
        controller.send_controller(128, 128, 128, 128, 0b00000000)  # Center position, no buttons pressed
        time.sleep(1)

        print("Controller: Top-Left")
        controller.send_controller(0, 0, 128, 128, 0b00000001)  # Top-left, Button 1 pressed
        time.sleep(1)

        print("Controller: Bottom-Right")
        controller.send_controller(255, 255, 128, 128, 0b00000010)  # Bottom-right, Button 2 pressed
        time.sleep(1)

        print("Controller: Trigger Pressed")
        controller.send_controller(128, 128, 255, 255, 0b00000100)  # Triggers max, Button 3 pressed
        time.sleep(1)

        print("Controller: Starting again...")


class XboxControllerInterface(HIDInterface):
    """USB HID interface for an Xbox-compatible controller."""

    def __init__(self):
        super().__init__(
            _XBOX_REPORT_DESC,
            set_report_buf=bytearray(6),  # X, Y, Z, Rz axes and buttons
            protocol=_INTERFACE_PROTOCOL_GAMEPAD,
            interface_str="MicroPython Xbox Controller",
        )

    def send_controller(self, x, y, z, rz, buttons):
        """Send Xbox controller data: X, Y, Z, Rz axes and buttons."""
        # Convert axis values (0-255)
        x = max(0, min(255, x))
        y = max(0, min(255, y))
        z = max(0, min(255, z))
        rz = max(0, min(255, rz))

        # Pack into a report: Axes (4 bytes) + Buttons (2 bytes)
        report = bytes([x, y, z, rz, buttons & 0xFF, (buttons >> 8) & 0xFF])
        self.send_report(report)


# HID Report descriptor for an Xbox-compatible controller
#
# fmt: off
_XBOX_REPORT_DESC = (
    b'\x05\x01'        # Usage Page (Generic Desktop)
    b'\x09\x05'        # Usage (Gamepad)
    b'\xA1\x01'        # Collection (Application)
        b'\x15\x00'    # Logical Minimum (0)
        b'\x26\xFF\x00'  # Logical Maximum (255)
        b'\x75\x08'    # Report Size (8 bits)
        b'\x95\x04'    # Report Count (4) - X, Y, Z, Rz
        b'\x05\x01'    # Usage Page (Generic Desktop)
        b'\x09\x30'    # Usage (X)
        b'\x09\x31'    # Usage (Y)
        b'\x09\x32'    # Usage (Z)
        b'\x09\x35'    # Usage (Rz)
        b'\x81\x02'    # Input (Data, Variable, Absolute)
        b'\x05\x09'    # Usage Page (Buttons)
        b'\x19\x01'    # Usage Minimum (1)
        b'\x29\x10'    # Usage Maximum (16)
        b'\x15\x00'    # Logical Minimum (0)
        b'\x25\x01'    # Logical Maximum (1)
        b'\x75\x01'    # Report Size (1 bit)
        b'\x95\x10'    # Report Count (16 buttons)
        b'\x81\x02'    # Input (Data, Variable, Absolute)
    b'\xC0'            # End Collection
)
# fmt: on


# Run the Xbox controller example
xbox_controller_example()
