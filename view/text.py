#!/usr/bin/env python3

import subprocess
import math

class Text:
    '''Text Class'''
    def __init__(self, settings):
        # Read Settings
        self.screen = settings['screen']

    def __number_sign(self, data):
        # Convert ' ' and  '#' to '0' and '1' (binary format)
        return data.translate(str.maketrans(' #', '01'))

    def get(self, text = '', font = 'banner'):
        width = self.screen['width']
        width_total = width * self.screen['total']
        height = self.screen['height']

        text_raw = subprocess.check_output(
            ['figlet', '-f', font, '-w', str(width_total), text],
            universal_newlines = True
        )

        text_lines = text_raw.splitlines()

        screens = math.ceil(len(max(text_lines, key = len)) / width)
        bit_map = [['' for h in range(len(text_lines))] for s in range(screens)]
        for h, w in enumerate(text_lines):
            # Truncate loop
            if h > height:
                break

            # Font selection
            if font == 'banner':
                line = self.__number_sign(w)
            else:
                line = ''

            count = 0
            width_max = min(len(line), width_total)
            for s in range(0, width_max, width):
                bit_map[count][h] = line[s:(s + width)]
                count += 1

        # Width and Length normalization
        data = ''
        for s in range(len(bit_map)):
            line = ''
            for l in range(len(bit_map[s])):
                line += bit_map[s][l] + '0' * (width - len(bit_map[s][l]))

            for l in range(height - len(bit_map[s])):
                line += '0' * width

            data += line

        # From Bits to Bytes
        bytes = [int(data[b:b + 8], 2) for b in range(0, len(data), 8)]

        return bytes