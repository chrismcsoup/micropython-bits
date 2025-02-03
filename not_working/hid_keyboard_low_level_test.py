from micropython import const
import time
from machine import Pin
import usb.device
from usb.device.hid import HIDInterface

_INTERFACE_PROTOCOL_KEYBOARD = const(0x01)
pin = Pin("LED", Pin.OUT)

def keypad_example():
    k = KeypadInterface()

    usb.device.get().init(k, builtin_driver=True)

    while not k.is_open():
        pin.toggle()
        time.sleep_ms(100)

    pin.on()
    while True:
        time.sleep(2)
        print("Press NumLock...")
        k.send_key("<NumLock>")
        time.sleep_ms(100)
        k.send_key()
        time.sleep(1)
        print("Press ...")
        for _ in range(3):
            time.sleep(0.1)
            k.send_key(".")
            time.sleep(0.1)
            k.send_key()
        print("Starting again...")


class KeypadInterface(HIDInterface):
    def __init__(self):
        super().__init__(
            _KEYPAD_REPORT_DESC,
            set_report_buf=bytearray(1),
            protocol=_INTERFACE_PROTOCOL_KEYBOARD,
            interface_str="MicroPython Keypad",
        )

    def send_key(self, key=None):
        if key is None:
            self.send_report(b"\x00")
        else:
            self.send_report(_key_to_id(key).to_bytes(1, "big"))


_KEYPAD_KEY_OFFS = const(0x53)
_KEYPAD_KEY_IDS = [
    "<NumLock>",
    "/",
    "*",
    "-",
    "+",
    "<Enter>",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    ".",
]

def _key_to_id(key):
    return _KEYPAD_KEY_IDS.index(key) + _KEYPAD_KEY_OFFS

_KEYPAD_REPORT_DESC = (
    b'\x05\x01'  # Usage Page (Generic Desktop)
        b'\x09\x07'  # Usage (Keypad)
    b'\xA1\x01'  # Collection (Application)
        b'\x05\x07'  # Usage Page (Keypad)
            b'\x19\x53'  # Usage Minimum (NumLock)
            b'\x29\x63'  # Usage Maximum (Keypad Keys)
            b'\x15\x00'  # Logical Minimum (0)
            b'\x25\x01'  # Logical Maximum (1)
            b'\x95\x01'  # Report Count (1),
            b'\x75\x08'  # Report Size (8),
            b'\x81\x00'  # Input (Data, Array, Absolute)
    b'\xC0'  # End Collection
)

keypad_example()
