# Activity 1 - I2C scanner + 16x2 I2C LCD   (ESP32-S3: SDA=GPIO8, SCL=GPIO9)
from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
devs = i2c.scan()

print("I2C DEVICE SCANNER")
print("Device:", "FOUND" if devs else "NOT FOUND")
if not devs:
    raise SystemExit
addr = devs[0]
print("Address: 0x%02X" % addr)
print("Status: CONNECTED")
print("Devices detected:", len(devs))


def pulse(b):                                  # PCF8574: P2=EN, P3=backlight
    i2c.writeto(addr, bytes([b | 0x0C])); time.sleep_us(500)
    i2c.writeto(addr, bytes([b | 0x08])); time.sleep_us(500)


def send(v, rs):                               # 8-bit value as two 4-bit nibbles
    pulse((v & 0xF0) | rs)
    pulse(((v << 4) & 0xF0) | rs)


for c in (0x33, 0x32, 0x28, 0x0C, 0x01):       # init -> 4-bit, 2 lines, clear
    send(c, 0); time.sleep_ms(5)


def show(row, text):
    send(0x80 | (0x40 * row), 0)
    for ch in "%-16s" % text:
        send(ord(ch), 1)


while True:
    show(0, "DEVICE: FOUND")
    show(1, "ADDR 0x%02X  CONN" % addr)
    time.sleep(2)
