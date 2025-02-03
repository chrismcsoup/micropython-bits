from machine import Pin
from time import ticks_ms, ticks_diff, sleep

class Debouncer:
    def __init__(self, pin: Pin, debounce_interval: int = 50):
        """
        Initialize the Debouncer for a button.

        :param pin: The Pin object for the button.
        :param debounce_interval: Debounce interval in milliseconds.
        """
        self.pin = pin
        self.debounce_interval = debounce_interval
        self.last_state = pin.value()  # Assume the current state is the stable state
        self.last_change_time = ticks_ms()

    def update(self):
        """
        Update the debouncer and check for a stable state change.

        :return: Tuple (state_changed, current_state)
                 state_changed: True if the stable state has changed.
                 current_state: The current stable state (0 for pressed, 1 for not pressed).
        """
        current_value = self.pin.value()
        now = ticks_ms()

        if current_value != self.last_state:
            # If state changed, check if debounce interval has passed
            if ticks_diff(now, self.last_change_time) > self.debounce_interval:
                self.last_state = current_value
                self.last_change_time = now
                return True, self.last_state

        return False, self.last_state

# Initialize LEDs and buttons
leds = [
    Pin(19, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(17, Pin.OUT),
    Pin(16, Pin.OUT)
]

buttons = [
    Pin(12, Pin.IN, Pin.PULL_UP),
    Pin(13, Pin.IN, Pin.PULL_UP),
    Pin(14, Pin.IN, Pin.PULL_UP),
    Pin(15, Pin.IN, Pin.PULL_UP),
]

# Create Debouncer instances for each button
debounced_btns = [Debouncer(button) for button in buttons]

while True:
    try:
        debug_msg =''
        for i, debouncer in enumerate(debounced_btns):
            # Update the debouncer and check for state changes
            state_changed, current_state = debouncer.update()

            if state_changed and current_state == 0:  # Button pressed
                leds[i].toggle()
            # Debug information
            debug_msg += f'B{i} -> changed: {state_changed}, cur_state: {current_state}; '

        print(debug_msg)
        sleep(0.01)  # Adjust for the desired loop frequency
    except KeyboardInterrupt:
        break

for led in leds:
    led.off()
print("Finished.")