from machine import Pin, PWM
import time

# GP4 pin, PWM
pump_pin = Pin(4, Pin.OUT)
pump_pwm = PWM(pump_pin)
pump_pwm.freq(65536)  # set frequency

def water(seconds_remaining=10, pump="No"):
    """
    Run the water pump for the remaining seconds.
    seconds_remaining: number of seconds pump should run
    pump: "Yes" to enable pump, "No" to stop
    """
    if pump == "Yes":
        pump_pwm.duty_u16(48768)  # 50% duty cycle (adjust if needed)
        start = time.time()
        while time.time() - start < seconds_remaining:
            time.sleep(0.1)  # keep loop light
        pump_pwm.duty_u16(0)  # turn off after time is up
    else:
        pump_pwm.duty_u16(0)  # make sure it's off
