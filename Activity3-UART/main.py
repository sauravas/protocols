# Activity 3 - UART command control  (UART1: TX=GPIO17, RX=GPIO18, 9600-8-N-1)
from machine import Pin, UART
import time

led = Pin(2, Pin.OUT)
uart = UART(1, 9600, bits=8, parity=None, stop=1, tx=Pin(17), rx=Pin(18))
uart.write("ESP32-S3 UART READY\r\n")

buf = b""
while True:
    if uart.any():
        buf += uart.read()
    if b"\n" in buf or b"\r" in buf:
        line, _, buf = buf.replace(b"\r", b"\n").partition(b"\n")
        cmd = line.decode().strip().upper()
        if cmd:
            uart.write(cmd + "\r\n")                      # echo
            if cmd == "LED ON":
                led.value(1); uart.write("LED TURNED ON\r\n")
            elif cmd == "LED OFF":
                led.value(0); uart.write("LED TURNED OFF\r\n")
            elif cmd == "STATUS":
                uart.write("SYSTEM OPERATIONAL\r\n")
            elif cmd == "HELP":
                uart.write("LED ON / LED OFF / STATUS / HELP\r\n")
            else:
                uart.write("UNKNOWN COMMAND\r\n")
    time.sleep_ms(20)
