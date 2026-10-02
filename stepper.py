# stepper_28byj.py — Raspberry Pi Pico (MicroPython)
# 28BYJ-48 stepper + ULN2003 driver
#
# Wiring:
#   GP21 → IN1, GP20 → IN2, GP19 → IN3, GP18 → IN4
# Power the motor from 5V; share GND with the Pico.

from machine import Pin
import time

# ---------------------------- Config ---------------------------------

# Coil pins in IN1..IN4 order (A, B, C, D)
_PINS = (
    Pin(21, Pin.OUT),  # IN1 ← GP21
    Pin(20, Pin.OUT),  # IN2 ← GP20
    Pin(19, Pin.OUT),  # IN3 ← GP19
    Pin(18, Pin.OUT),  # IN4 ← GP18
)

# Half-step sequence (smooth, higher torque) for IN1..IN4
_HALFSTEP = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1),
)

_STEP_DELAY_MS   = 1       # 2–5 ms typical for 28BYJ-48
_DEFAULT_SECONDS = 20    # spin time for "Up"/"Down"
_UP_IS_CLOCKWISE = True    # flip if your mechanical Up is CCW

# Precompute forward/backward sequences without slice steps (uPy-safe)
_CW_SEQ  = _HALFSTEP
_CCW_SEQ = tuple(reversed(_HALFSTEP))

# ------------------------- Low-level drive ---------------------------

def _energize(pattern) -> None:
    for pin, val in zip(_PINS, pattern):
        pin.value(val)

def _release() -> None:
    for p in _PINS:
        p.value(0)

def _spin(sequence, seconds: float) -> None:
    end = time.ticks_add(time.ticks_ms(), int(seconds * 1000))
    i = 0
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        _energize(sequence[i & 7])  # fast modulo 8
        time.sleep_ms(_STEP_DELAY_MS)
        i += 1
    _release()

# --------------------------- Public API ------------------------------

def stepper(direction: str) -> None:
    """
    Rotate for 3 seconds in the requested direction.

    Args:
        direction: "Up"/"U"    → clockwise (by default)
                   "Down"/"D"  → counter-clockwise

    Notes:
        - Set _UP_IS_CLOCKWISE=False if your mechanism defines Up as CCW.
        - Increase _STEP_DELAY_MS for more torque; decrease for more speed.
    """
    d = (direction or "").strip().lower()
    if d not in ("up", "u", "down", "d"):
        raise ValueError('direction must be "Up"/"U" or "Down"/"D"')

    if _UP_IS_CLOCKWISE:
        seq = _CW_SEQ if d in ("up", "u") else _CCW_SEQ
    else:
        seq = _CCW_SEQ if d in ("up", "u") else _CW_SEQ

    _spin(seq, _DEFAULT_SECONDS)

# ---------------------------- Demo ----------------------------------

if __name__ == "__main__":
    stepper("Up")
    time.sleep(0.4)
    stepper("Down")
