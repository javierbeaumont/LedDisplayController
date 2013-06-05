#!/usr/bin/env python3

import argparse
import io
import struct

# View
import view.text

# Frames
import frame.control
import frame.data

# Serial Port
import inout.serial

class StandardInput:
    '''Standard Input'''

    def __init__(self, settings):
        # Read Settings
        self.settings = settings

        parser = argparse.ArgumentParser(
            description = 'Process some integers.',
            epilog = 'LedDisplayController home page: '
            '<https://github.com/javierbeaumont/LedDisplayController/>',
            formatter_class = argparse.RawTextHelpFormatter,
            add_help = True
        )

        parser.add_argument(
            '-v', '--version',
            action = 'version',
            version = '%(prog)s 0.0.2'
        )

        parser.add_argument(
            '-t', '--text',
            type = str,
            help = 'Text to show',
        )

        parser.add_argument(
            '-f', '--font',
            type = str,
            help = 'Text font',
        )

        parser.add_argument(
            '-i', '--input-file',
            type = argparse.FileType('rb'),
            help = 'Read input data from FILE (binary)',
            metavar = 'FILE'
        )

        parser.add_argument(
            '-o', '--output-file',
            type = argparse.FileType('wb'),
            help = 'Write output data to FILE (binary). '
            'If FILE is "-" print to the standard output ',
            metavar = 'FILE'
        )

        parser.add_argument(
            '-d', '--data-format',
            nargs = 2,
            default = ['b', 'b'],
            type = str,
            choices = ['b', '0', 'h'],
            help = 'Data Input/Output format. Allowed values:\n'
            '- b: Binary format\n'
            '- 0: Binary (0..1)\n'
            '- h: Hexadecimal (00..ff)\n'
            'Example: -f d h (input decimal data, output hexadecimal data)',
            metavar = ('INPUT_FORMAT', 'OUTPUT_FORMAT'),
            dest='format'
        )

        parser.parse_args(namespace = self)

    def __format(self, data, format):
        base = {
            '0': {'digits':  2, 'format': '{:0>8b}'},
            'h': {'digits': 16, 'format': '{:0>2x}'}
        }

        io_format = {'input': self.format[0], 'output': self.format[1]}
        io_format.update(format)

        if io_format['input'] == io_format['output']:
            return data;
        else:
            if io_format['input'] == 'b':
                bytes = struct.unpack('%sB' % len(data), data)
            elif io_format['input'] == 'd':
                bytes = data
            else:
                group = data.split()

                base_digits = base[io_format['input']]['digits']

                bytes = []
                for i in range(len(group)):
                    bytes.append(int(group[i], base_digits))

            if io_format['output'] == 'b':
                return struct.pack('%sB' % len(bytes), *bytes)
            else:
                base_format = base[io_format['output']]['format']

                group = []
                for i in range(len(bytes)):
                    group.append(base_format.format(bytes[i]))

                return ' '.join(group)

    def input(self):
        if isinstance(self.input_file, io.BufferedReader):
            io_file = io.BufferedReader(self.input_file)
            return io_file.read()
        elif self.text:
            text = view.text.Text(self.settings)
            if self.font:
                return text.get(self.text, font)
            else:
                return text.get(self.text)
        else:
            print ('server')

    def output(self, data):
        if isinstance(self.output_file, io.BufferedWriter):
            data_format = self.__format(data)
            if not isinstance(data_format, bytes):
                data_write = data_format.encode('utf-8')
            else:
                data_write = data_format

            io_file = io.BufferedWriter(self.output_file)
            io_file.write(data_write)
            io_file.close()
        elif isinstance(self.output_file, io.TextIOWrapper):
            print(self.__format(data))
        else:
            # Data Frame
            data_frame = frame.data.DataFrame(self.settings)
            data_data = data_frame.get(data)

            # Control Frame
            control_frame = frame.control.ControlFrame(self.settings, data_data['screen'])
            data_control = control_frame.get()

            bytes_list = data_control['data'] + data_data['data']

            # Send bynary data to leds
            in_out = inout.serial.SerialPort(self.settings)
            in_out.send(data_data['screen'], self.__format(bytes_list, {'input': 'd'}))