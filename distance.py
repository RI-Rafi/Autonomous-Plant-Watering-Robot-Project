from machine import Pin, time_pulse_us
import utime

# Pin setup
TRIG = Pin(0, Pin.OUT)
ECHO = Pin(1, Pin.IN)

def measure_distance():
    # Ensure trigger is low
    TRIG.low()
    utime.sleep_us(2)

    # Send 10µs pulse
    TRIG.high()
    utime.sleep_us(10)
    TRIG.low()

    # Measure echo pulse duration
    duration = time_pulse_us(ECHO, 1, 30000)  # timeout after 30ms
    
    if duration < 0:
        return None  # Timeout (no object detected)

    # Convert to distance (cm)
    distance_cm = (duration / 2) * 0.0343
    return distance_cm

# Example usage