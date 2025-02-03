# This is a midi trs A test based on this blog post: https://barbarach.com/midi-control-pedal-the-beginning/
# We are using the micropython-midi-library from sensai7 https://github.com/sensai7/Micropython-midi-library

# Wiring:  
# PICO UART0 TX (PIN 0) --> 10R --> Tip of TRS Jack
# PICO 3V3 --> 33R (I used a 47R and it also works) --> Ring of TRS Jack
# PICO GND --> Sleeve of TRS Jack



from machine import Pin
from utime import sleep
from lib.midi import Midi, CHANNEL, NOTE_CODE, CONTROL_CHANGE_CODE

pin = Pin("LED", Pin.OUT) # for debugging, pico w's internal led

MIDI_TX = Pin(0)             # MIDI output in general purpose pin 0 (UART0 TX)
MIDI_RX = Pin(1)             # This is not used/connected at the moment but needed for MIDI Out if you want
UART_0 = 0
my_midi = Midi(UART_0, tx=MIDI_TX, rx=MIDI_RX)

START_NOTE= 60 # C4
note = START_NOTE

while True:
    try:
        pin.toggle()
        my_midi.send_note_on(CHANNEL[1], note , velocity=100) # type: ignore
        my_midi.send_note_off(CHANNEL[1], note) # type: ignore
        my_midi.send_control_change(CHANNEL[1], CONTROL_CHANGE_CODE["MODULATION_WHEEL"], value=80) # type: ignore

        # increase note every loop
        note += 1
        if note >= 90: 
            note = START_NOTE
        sleep(1)
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")