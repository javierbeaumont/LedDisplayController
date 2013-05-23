#!/usr/bin/env python3

class New:
    """A Data Frame class"""

    SIGN = {
        'redFirst': 0x7f,
        'greenFirst': 0x6f,
        'redMiddle': 0x7e,
        'greenMiddle': 0x6e,
        'redLast': 0x7d,
        'greenLast': 0x6d
    }

    displayNumber = 0

    def __init__(self, displayNumber = 0):
        self.displayNumber = displayNumber

    def bytes(self, data = [], sign = 'redFirst'):
        bytes = [
            self.displayNumber,
            int(self.SIGN[sign]),
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ] + data

        for i in range(len(data) + 11, 1000):
            bytes += [0]

        bytes += [sum(bytes) % 256]

        return bytes