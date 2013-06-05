#!/usr/bin/env python3

class ControlFrame:
    '''A Control Frame class'''

    def __init__(self, settings, screen = {}, mode = []):
        # Define screnn and mode bytes
        self.data_bytes = {
            'screen': {
                0: 'number',
                1: 'sign',
                2: 'amount',
                4: 'first',
                5: 'last',
                6: 'width',
                7: 'height',
                8: 'color',
                9: 'total',
                10: 'sdv'
            },
            'mode': {
                11: 'leadin',
                12: 'leadout',
                13: 'delay',
                14: 'speed',
                15: 'append',
                16: 'animation'
            },
            'amount': {
                'mode': 6
            }
        }

        # Define append bits
        self.data_bits = {
            'append': {
                0: 'animation',
                1: 'repose',
                3: 'time',
                4: 'continous',
                5: 'pause',
                7: 'winkle'
            }
        }

        # Read Control Frame Settings
        self.screen = settings['screen']

        # Define Screen (Control Frame Sign: 0x5f)
        self.screen.update({'sign': 95, 'amount': 1, 'sdv': 1})

        self.screen.update(screen)
        self.screen['width'] = round(self.screen['width'] / 8)
        self.screen['height'] = round(self.screen['height'] / 8)

        # Define Screen Mode
        self.mode = [{'delay': 10, 'append': {}}] * self.screen['amount']

        for i in range(min(self.screen['amount'], len(mode))):
            self.mode[i].update(mode[i])

        # Define Frame Layout
        self.frames = settings['frames']['bytes']
        self.bytes = [0] * sum(self.frames.values())

    def get(self):
        for (byte, name) in self.data_bytes['screen'].items():
            self.bytes[byte] = self.screen.get(name, 0)

        for i in range(self.screen['amount']):
            append_mode = ['0'] * 8

            for (bit, name) in self.data_bits['append'].items():
                append_mode[bit] = str(self.mode[i]['append'].get(name, 0))

            c = self.data_bytes['amount']['mode']
            for (byte, name) in self.data_bytes['mode'].items():
                if name == 'append':
                    value = int(''.join(append_mode), 2)
                else:
                    value = self.mode[i].get(name, 0)
                self.bytes[i * c + int(byte)] = value

        byte = sum(self.frames.values()) - self.frames['checksum']
        self.bytes[byte] = sum(self.bytes) % 256

        return         return {
            'data': self.bytes,
            'screen': {
                'number': self.bytes[0]
            }
        }