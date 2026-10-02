from machine import Pin, I2C
import utime

# I2C setup for LCD (SDA = GP2, SCL = GP3)
i2c = I2C(1, scl=Pin(1), sda=Pin(2), freq=400000)

# Import I2C LCD library
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Scan for I2C devices
I2C_ADDR = i2c.scan()[0]   # automatically pick the first device found
print("I2C Address:", hex(I2C_ADDR))

# Initialize LCD (16x2)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Display message
lcd.putstr("Hello World")

while True:
    utime.sleep(1)
