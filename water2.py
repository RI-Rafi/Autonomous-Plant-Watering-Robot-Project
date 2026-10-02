from machine import Pin, PWM
import time
from dist2 import measure_dist2
from buzzer import buzz
# GP5 pin, PWM
pump_pin = Pin(5, Pin.OUT)
pump_pwm = PWM(pump_pin)
pump_pwm.freq(65536)  # set frequency

def water2(seconds_remaining=10, pump="No"):
    """
    Run the water pump for the remaining seconds.
    seconds_remaining: number of seconds pump should run
    pump: "Yes" to enable pump, "No" to stop
    """
    print(seconds_remaining, 'water2')
    x = measure_dist2() 
    print(x)
    if pump == "Yes" and x < 4:
        buzz(True)
        pump_pwm.duty_u16(48768)  # 50% duty cycle (adjust if needed)
        start = time.time()
        while time.time() - start < seconds_remaining:
            time.sleep(0.1)  # keep loop light
        pump_pwm.duty_u16(0)  # turn off after time is up
    else:
        buzz()
        pump_pwm.duty_u16(0)  # make sure it's off

