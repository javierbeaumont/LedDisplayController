#!/usr/bin/env python3

import serial

class SerialPort:
    def __init__(self, settings):
        # Read Serial Port
        self.port = settings['output']['port']

    def send(self, screen, data):
        if screen:
            write = [screen, data]
            timeout = None
        else:
            write = [data]
            timeout = 0

        # Configure port
        led = serial.Serial(
            self.port,
            baudrate = 19200,
            stopbits = serial.STOPBITS_TWO,
            timeout = timeout
        )

        for d in range(write)
            # Write data
            led.write(d)

            # Read data (TODO)
            r = led.read()
            print(r)

        # Close port
        led.close()

        return True