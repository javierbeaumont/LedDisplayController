#!/usr/bin/env python3

import serial

class SerialPort:
    def __init__(self, settings):
        # Read Serial Port
        self.port = settings['output']['port']

    def send(self, data):
        # Configure port
        led = serial.Serial(
            self.port,
            baudrate = 19200,
            stopbits = serial.STOPBITS_TWO,
            timeout = 0
        )

        # Write data
        led.write(data)

        # Read data (TODO)
        r = led.read()
        print(r)

        # Close port
        led.close()

        return True