# This is a midi trs A test based on this blog post: https://barbarach.com/midi-control-pedal-the-beginning/
# We are using the micropython-midi-library from sensai7 https://github.com/sensai7/Micropython-midi-library
# I wanted to make a touch sensor to trigger a the volca drum synthesizer by finger drumming
# but it turns out the pi pico internal ADC is not usable because of a 150khz noise from the 
# switching power converter that interferes with the signals from the touch sensor.
# This whole test was inspired by this video: https://youtu.be/_RUZtsQzSLY?si=L7p9L8D5CHV69xIm
# I think it might work with an external ADC like mcp3204 or mcp3208

# Wiring:  
# PICO UART0 TX (PIN 0) --> 10R --> Tip of TRS Jack
# PICO 3V3 --> 33R (I used a 47R and it also works) --> Ring of TRS Jack
# PICO GND --> Sleeve of TRS Jack



from machine import Pin, ADC
from utime import sleep, ticks_diff, ticks_ms, sleep_ms
from lib.midi import Midi, CHANNEL, NOTE_CODE, CONTROL_CHANGE_CODE



pin = Pin("LED", Pin.OUT) # for debugging, pico w's internal led

MIDI_TX = Pin(0)             # MIDI output in general purpose pin 0 (UART0 TX)
MIDI_RX = Pin(1)             # This is not used/connected at the moment but needed for MIDI Out if you want
UART_0 = 0
my_midi = Midi(UART_0, tx=MIDI_TX, rx=MIDI_RX)
channel = 6
velocity = 0
touch_sensor = ADC(27)

# Configuration
ALPHA = 0.05  # EMA smoothing factor (smooths baseline slowly)
THRESHOLD = 2800  # Expected drum hit amplitude (~150mV)
DEBOUNCE_TIME = 150  # Time to prevent multiple detections from one hit
VELOCITY_MAX = 127  # Max velocity value (e.g., for MIDI mapping)
SENSOR_MAX = 5000  # Adjust to match expected max hit strength

# Baseline estimation variables
baseline = touch_sensor.read_u16()  # Initial baseline
last_event_time = 0

def read_filtered_adc(adc):
    """Reads ADC value, applies EMA filtering, detects drum hits, and returns velocity."""
    global baseline, last_event_time
    
    # Read raw ADC value
    raw_value = adc.read_u16()

    # Update baseline with an exponential moving average
    baseline = (ALPHA * raw_value) + ((1 - ALPHA) * baseline)

    # Calculate high-pass filtered signal (deviation from baseline)
    filtered_value = abs(raw_value - baseline)

    # Detect sudden spikes
    if filtered_value > THRESHOLD:
        current_time = ticks_ms()
        if ticks_diff(current_time, last_event_time) > DEBOUNCE_TIME:
            # Normalize velocity
            velocity = min(int((filtered_value / SENSOR_MAX) * VELOCITY_MAX), VELOCITY_MAX)
            
            print(f"Drum Hit Detected! Value: {raw_value}, Velocity: {velocity}")
            
            last_event_time = current_time  # Update debounce timer
            
            return velocity  # Return hit intensity
    
    return 0  # Return 0 if no hit detected

while True:
    try:
        #pin.toggle()
        #my_midi.send_note_on(channel, 60 , velocity=velocity) # type: ignore
        #my_midi.send_note_off(channel, 60) # type: ignore
        #print(f"velocity:{velocity}")
        # increase note every loop
        # velocity += 10
        # if velocity >= 127: 
        #     velocity = 0
        # print(touch_sensor.read_u16())
        #sleep(0.3)
        velocity = read_filtered_adc(touch_sensor)
        if velocity > 0:
            # Process velocity (e.g., send via MIDI, store in array, etc.)
            pass
        sleep_ms(5)  # Adjust based on sampling needs
    except KeyboardInterrupt:
        break
pin.off()
print("Finished.")