#!/usr/bin/env python3

import subprocess

class Text:
    '''Text Class'''
    def __init__(self, settings):
        # Read Settings
        self.screen = settings['screen']

    def __number_sign(self, data):
        # Convert ' ' and  '#' to '0' and '1' (binary format)
        return data.translate(str.maketrans(' #', '01'))

    def get(self, text = '', font = 'banner'):
        length = self.screen['width'] * self.screen['total']
        rawData = subprocess.check_output(
            ['figlet', '-f', font, '-w', str(length), text],
            universal_newlines = True
        )

        data = rawData.splitlines()
        for (k, l) in enumerate(data):
            # Font selection
            if font == 'banner':
                line = self.__number_sign(l)
            else:
                line = ''

            # Length normalization
            line += '0' * (8 - len(line) % 8)

            data[k] = [int(line[b:b + 8], 2) for b in range(0, len(line), 8)]

            # Truncate loop
            if (k + 1 == self.screen['height']):
                break

        return data