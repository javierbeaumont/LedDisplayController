#!/usr/bin/env python3

import subprocess

class Text:

    LENGTH = 150
    HEIGHT = 16
    DATABYTES = 990

    # Convert ' ' and  '#' to '0' and '1' (binary format)
    def number_sign(self, data):
        return data.translate(str.maketrans(' #', '01'))

    def get(self, text = '', font = 'banner'):
        rawData = subprocess.check_output(['figlet', '-f', font, '-w', str(self.LENGTH), text], universal_newlines=True)

        lines = rawData.splitlines()

        for (i, line) in enumerate(lines):
            # Font selection
            if font == 'banner':
                line = self.number_sign(line)
            else:
                line = ''

            # Truncate line
            if len(line) > self.LENGTH:
                line = line[:(self.LENGTH -1)]
            else:
                line = '{:0^150}'.format(line)

            lines[i] = line

            # Truncate loop
            if (i + 1 == self.HEIGHT):
                break

        data = ''.join(lines)

        i += 1

        if (i < self.HEIGHT):
            data += '0' * self.LENGTH * (self.HEIGHT - i)

        dataBytes =  round(len(data) / 8)

        if (dataBytes < self.DATABYTES):
            data += '0' * 8 * (self.DATABYTES - dataBytes)

        print ('\n'.join(lines).translate(str.maketrans('01', '.#')))

        return [int(data[i:i + 8], 2) for i in range(0, len(data), 8)]