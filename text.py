#!/usr/bin/env python3

import subprocess, struct

LENGTH = 150
HEIGHT = 16
DATABYTES = 990

font = 'banner'

text = 'Hello World!'

filename = 'examples/test.bin'
    
rawData = subprocess.check_output(['figlet', '-f', font, '-w', str(LENGTH), text], universal_newlines=True)

print (rawData.translate(str.maketrans(' ', '.')))

lines = rawData.splitlines()

# Convert ' ' and  '#' to '0' and '1' (binary format)
def numberSign(data):
    return data.translate(str.maketrans(' #', '01'))

for (i, line) in enumerate(lines):
    # Font selection
    if font == 'banner':
        line = numberSign(line)
    else:
        line = ''

    # Truncate line
    if len(line) > LENGTH:
        line = line[:(LENGTH -1)]
    else:
      line = '{:0<150}'.format(line)

    lines[i] = line

    # Truncate loop
    if (i + 1 == HEIGHT):
        break

data = ''.join(lines)

i += 1

if (i < HEIGHT):
    data += '0' * LENGTH * (HEIGHT - i)

dataBytes =  round(len(data) / 8)

if (dataBytes < DATABYTES):
    data += '0' * 8 * (DATABYTES - dataBytes)

bytes = [int(data[i:i + 8], 2) for i in range(0, len(data), 8)]

binary = struct.pack('%sB' % len(bytes), *bytes)

print(binary)

# TODO Send to led
print(filename)
f = open(filename, 'wb')
f.write(binary)
f.close()