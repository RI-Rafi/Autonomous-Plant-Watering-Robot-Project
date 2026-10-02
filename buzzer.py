from machine import Pin, PWM
import time

# Passive buzzer on GP18
buzzer = PWM(Pin(28))
red = PWM(Pin(6))
def buzz(val = False):
    if val:
        buzzer.freq(1000)   # Set frequency to 1 kHz
        buzzer.duty_u16(20000)  # Set duty cycle (~50%)
        time.sleep(1)     # Play tone for 0.5 sec
        buzzer.duty_u16(0)  # Turn OFF buzzer
        time.sleep(0.5)
        val = False
    else:
        red.freq(1000)   # Set frequency to 1 kHz
        red.duty_u16(10000)  # Set duty cycle (~50%)
        time.sleep(1)     # Play tone for 0.5 sec
        red.duty_u16(0)  # Turn OFF buzzer
        time.sleep(0.5)
        
    return 0
