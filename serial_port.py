#!/usr/bin/env python3

import serial

# TODO Own data
file = open('examples/test.bin', 'rb')
data = file.read()

PORT = '/dev/ttyUSB0'

led = serial.Serial(PORT, baudrate = 19200, stopbits = serial.STOPBITS_TWO, timeout = 0) # Configure port

led.write(data) # Write data

# TODO Fix Read data
r = led.read() # Write data
print(r)

led.close() # Close port