#!/usr/bin/env python3

import math

class DataFrame:
    """A Data Frame class"""

    SIGN = [0x7f, 0x6f, 0x7e, 0x6e, 0x7d, 0x6d]

    def __init__(self, settings, display_number = 0):
        self.width = round(settings['screen']['width'] / 8)
        self.height = settings['screen']['height']
        self.frames_bytes = settings['frames']['bytes']

        # Define Display Number
        self.display_number = display_number

        # Define Frame Layout
        self.frames_total_bytes = sum(self.frames_bytes.values())

    def get(self, data = []):
        frame_data = []
        frames = max(2, 2)
        for f in range(frames):
            bytes = [0] * self.frames_total_bytes
            if f == 0:
                sign = self.SIGN[0]
                data_bytes = data
            elif f + 1 == frames:
                sign = self.SIGN[4]
                data_bytes = [0]
            else:
                sign = self.SIGN[2]
                data_bytes = [0]

            bytes[0] = self.display_number
            bytes[1] = int(sign)

            bytes[11:len(data_bytes) + 11] = data_bytes

            checksum = self.frames_bytes['checksum']
            bytes[self.frames_total_bytes - checksum] = sum(bytes) % 256

            frame_data += bytes

        return {
            'data': frame_data,
            'screen': {
                'amount': frames,
                'last': frames - 1
            }
        }