#!/usr/bin/env python3

# Settings
import configparser

# Input
import inout.standard

# Settings data
config = configparser.ConfigParser()
config.read('settings.ini')

settings = dict(config._sections)
for key, value in settings.items():
    i = dict(value).items()
    settings[key] = dict((k, int(v) if v.isdigit() else v) for k, v in i)

settings.update({
    "frames": {
        "bytes": {
            "header": 11,
            "data": 990,
            "checksum": 1
        }
    }
})

# Input / output
in_out = inout.standard.StandardInput(settings)
data = in_out.input()

# Output
in_out.output(data)