# MicroPython USB Keyboard example
#
# To run this example:
#
# 1. Check the KEYS assignment below, and connect buttons or switches to the
#    assigned GPIOs. You can change the entries as needed, look up the reference
#    for your board to see what pins are available. Note that the example uses
#    "active low" logic, so pressing a switch or button should switch the
#    connected pin to Ground (0V).
#
# 2. Make sure `usb-device-keyboard` is installed via: mpremote mip install usb-device-keyboard
#
# 3. Run the example via: mpremote run keyboard_example.py
#
# 4. mpremote will exit with an error after the previous step, because when the
#    example runs the existing USB device disconnects and then re-enumerates with
#   the keyboard interface present. At this point, the example is running.
#
# 5. The example doesn't print anything to the serial port, but to stop it first
#    re-connect: mpremote connect PORTNAME
#
# 6. Type Ctrl-C to interrupt the running example and stop it. You may have to
#    also type Ctrl-B to restore the interactive REPL.
#
# To implement a keyboard with different USB HID characteristics, copy the
# usb-device-keyboard/usb/device/keyboard.py file into your own project and modify
# KeyboardInterface.
#
# MIT license; Copyright (c) 2024 Angus Gratton
import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode, LEDCode
from machine import Pin
import time

pin = Pin("LED", Pin.OUT)

class ExampleKeyboard(KeyboardInterface):
    pass

def keyboard_example():
    
    
    # Register the keyboard interface and re-enumerate
    k = ExampleKeyboard()
    usb.device.get().init(k, builtin_driver=True)

    print("Entering keyboard loop...")

    while True:

        if k.is_open():            
            pin.on()
            k.send_keys([KeyCode.DOT])
            time.sleep_ms(500)
        else:
            pin.toggle()
            time.sleep_ms(100)

        # This simple example scans each input in an infinite loop, but a more
        # complex implementation would probably use a timer or similar.
        time.sleep_ms(1)


keyboard_example()