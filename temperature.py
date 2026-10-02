from machine import ADC
import time
from distance import measure_distance
# Set your temperature band (example values)
T_LOW  = 24.0   # start scaling at 24°C
T_HIGH = 50.0   # max water at 34°C

TOTAL_SECONDS = 20.0
# ADC4 is the internal temperature sensor
adc = ADC(4)
CONV = 3.3 / 65535  # ADC -> volts

def temp(samples=10, delay_ms=10):
    """Return averaged die temperature in °C."""
    acc = 0
    for _ in range(samples):
        acc += adc.read_u16()
        time.sleep_ms(delay_ms)
    raw = acc // samples
    voltage = raw * CONV
    # From RP2040 datasheet: 27°C at 0.706 V, slope ≈ 1.721 mV/°C
    temp_c = 27 - (voltage - 0.706) / 0.001721
    return temp_c
def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def water_seconds_from_temp(T, Tlow=T_LOW, Thigh=T_HIGH, total=TOTAL_SECONDS):
    if Thigh <= Tlow:
        # safety: avoid divide-by-zero; default to all-or-nothing
        return total if T >= Thigh else 0.0
    frac = (T - Tlow) / (Thigh - Tlow)
    seconds = frac * total
    return clamp(seconds, 0.0, total)

def run_cycle():
    T = temp()
    pot_hieght = measure_distance()/10
    seconds = water_seconds_from_temp(T) + pot_hieght
    print(f"Die temp: {T:.2f} °C -> watering {seconds:.1f} s")
    if seconds > 0:
        return seconds
