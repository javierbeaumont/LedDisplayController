#!/usr/bin/env python3

import serial

class Send:
    PORT = '/dev/ttyUSB0'

    def data(self, data):
        # Configure port
        led = serial.Serial(self.PORT, baudrate = 19200, stopbits = serial.STOPBITS_TWO, timeout = 0)

        # Write data
        led.write(data)

        # Read data (TODO fix)
        r = led.read()
        print(r)

        # Close port
        led.close()

        return True