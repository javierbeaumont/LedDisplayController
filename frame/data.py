#!/usr/bin/env python3

import math

class DataFrame:
    """A Data Frame class"""

    SIGN = [0x7f, 0x6f, 0x7e, 0x6e, 0x7d, 0x6d]

    def __init__(self, settings, display_number = 0):
        self.width =  settings['screen']['width']
        self.height =  settings['screen']['height']
        self.frames_bytes = settings['frames']['bytes']

        # Define Display Number
        self.display_number = display_number

        # Define Frame Layout
        self.frames_total_bytes = sum(self.frames_bytes.values())
        self.bytes = [0] * self.frames_total_bytes

    def get(self, data = []):
        data_bytes = []
        for h in range(len(data)):
            i = 0
            data_bytes_rows = []
            while len(data[h]):
                data_width = min(self.width, len(data[h]))
                data_bytes_rows.append(
                    data[h][:data_width] + [0] * (self.width - data_width)
                )
                data[h] = data[h][data_width:]
                i += 1

            data_bytes.append(data_bytes_rows)

        count = 0
        data_format = []
        for col in zip(*data_bytes):
            data_format_frame = []
            for row in col:
                data_format_frame += row
                count += len(row)

            data_format.append(data_format_frame)


        bytes = self.bytes

        frame_data = []
        frames = max(math.ceil(count / (self.frames_bytes['data'])), 2)
        for f in range(frames):
            if f == 0:
                sign = self.SIGN[0]
            elif f + 1 == frames:
                sign = self.SIGN[5]
            else:
                sign = self.SIGN[3]

            bytes[0] = self.display_number
            bytes[1] = int(sign)
            bytes[2:len(data_format[f])] = data_format[f]

            checksum = self.frames_bytes['checksum']
            bytes[self.frames_total_bytes - checksum] = sum(bytes) % 256

            frame_data += bytes

        return frame_data