#!/usr/bin/env python3

import sys

import view.text

import frame.control
import frame.data

import struct

import serial_port

# Create content
font = 'banner'

text_class = view.text.Text()
code = text_class.get(sys.argv[1], font)

# Create frames
data = []

control_frame = frame.control.New()
data += control_frame.bytes()

data_frame = frame.data.New()
data += data_frame.bytes(code, 'redFirst')
data += data_frame.bytes([], 'redLast')

# Create binary data
binary = struct.pack('%sB' % len(data), *data)

# Send data
send = serial_port.Send()
send.data(binary)