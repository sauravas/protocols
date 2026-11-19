# Activity 2 - SPI master transmission  (SCK=12, MOSI=11, MISO=13, CS=10)
# MOSI is looped back to MISO so the received bytes can be checked.
from machine import Pin, SPI
import time

cs = Pin(10, Pin.OUT, value=1)                 # CS idles HIGH
spi = SPI(1, baudrate=100000, polarity=0, phase=0, bits=8,
          sck=Pin(12), mosi=Pin(11), miso=Pin(13))

data = bytes([0x55, 0xAA, 0x10, 0x25])

print("SPI TRANSMISSION")
print("100 kHz, 8-bit, MSB first, Mode 0")
print("TX DATA: " + " ".join("%02X" % b for b in data))

while True:
    rx = bytearray(len(data))
    cs.value(0)                                # select slave
    spi.write_readinto(data, rx)               # clock out MOSI / clock in MISO
    cs.value(1)                                # deselect slave
    print("RX DATA: " + " ".join("%02X" % b for b in rx))
    print("SPI: TRANSMISSION COMPLETE")
    time.sleep(2)
