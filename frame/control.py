#!/usr/bin/env python3

class New:
    """A Control Frame class"""

    SIGN = 0x5f

    screen = {
        'number': 0,
        'amount': 1,
        'first': 0,
        'last': 0,
        'length': 128,
        'height': 16,
        'color': 1,
        'maximumAmount': 150,
        'displaySdv': 1
    }

    mode = {
        'leadIn': 0,
        'leadOut': 0,
        'timeDelay': 10,
        'speed': 0,
        'append': {
            'animation': 0,
            'repose': 0,
            'time': 0,
            'continous': 0,
            'pause': 0,
            'winkle': 0
        },
        'animation': 0
    }

    modeList = []

    def __init__(self, screen = {}, mode = []):
        self.screen.update(screen)

        self.modeList = [self.mode for i in range(self.screen['amount'])]

        for i in range(self.screen['amount']):
            if i < len(mode):
                self.modeList[i].update(mode[i])

    def bytes(self):
        bytes = [
            self.screen['number'],
            int(self.SIGN),
            self.screen['amount'],
            0,
            self.screen['first'],
            self.screen['last'],
            round(self.screen['length'] / 8),
            round(self.screen['height'] / 8),
            self.screen['color'],
            self.screen['maximumAmount'],
            self.screen['displaySdv']
        ]

        count = 10

        for i in range(self.screen['amount']):
            mode = self.modeList[i]
            append = mode['append']

            append = ''.join([
                str(mode['append']['animation']),
                str(mode['append']['repose']),
                '0',
                str(mode['append']['time']),
                str(mode['append']['continous']),
                str(mode['append']['pause']),
                '0',
                str(mode['append']['winkle'])
            ])

            bytes += [
                mode['leadIn'],
                mode['leadOut'],
                mode['timeDelay'],
                mode['speed'],
                int(append, 2),
                mode['animation']
            ]

            count += 6

        for i in range(count, 1000):
            bytes += [0]

        bytes += [sum(bytes) % 256]

        return bytes