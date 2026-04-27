# LedDisplayController

Python controller for the **LED 16×128 Multi-Language Moving Sign** — a serial-connected LED matrix display. Converts text and binary data into the display's native frame protocol and transmits it over USB-to-serial.

> **Hardware note:** This project targets a specific piece of discontinued hardware. I no longer have access to the device, but the code works and is left public in case someone with the same hardware finds it useful.

---

## Hardware

| Property | Value |
|---|---|
| Display dimensions | 16 px × 128 px |
| Connection | USB-to-serial adapter (`/dev/ttyUSB0`) |
| Baud rate | 19200 |
| Stop bits | 2 |
| Parity | None |
| Max display number | 255 |

The display is sold under several names:
- LED 16×128
- LED Multi-line Message Display
- LED Multi-Language Moving Sign (internal software name: *Dztp*)

### Display variants

| Variant | Colors | Max width |
|---|---|---|
| Single color | Red, black | 64 px |
| Double color | Red, green, yellow, black | 32 px |

---

## Requirements

- Python 3.x
- [`pySerial`](https://pyserial.readthedocs.io/)
- [`figlet`](http://www.figlet.org/) (system package, used for text rendering)

Install dependencies:

```bash
pip install pyserial
# Debian/Ubuntu
sudo apt install figlet
# macOS
brew install figlet
```

---

## Configuration

Edit `settings.ini` before use:

```ini
[output]
port=/dev/ttyUSB0      # Serial port of the USB-to-serial adapter

[screen]
color=1                # Display color mode
width=128              # Display width in pixels
height=16              # Display height in pixels
total=150              # Total number of displayable screens
```

---

## Usage

```
main.py [-v] [-t TEXT] [-f FONT] [-i FILE] [-o FILE] [-d INPUT_FORMAT OUTPUT_FORMAT]
```

| Flag | Description |
|---|---|
| `-t TEXT` | Text to display |
| `-f FONT` | FIGlet font name (default: `banner`) |
| `-i FILE` | Read pixel data from a binary file |
| `-o FILE` | Write output to a file instead of the display |
| `-d FMT_IN FMT_OUT` | Convert between data formats: `b` (binary), `0` (ASCII binary), `h` (hexadecimal) |
| `-v` | Verbose output |

### Examples

Display text using the default font:
```bash
python main.py -t "Hello"
```

Display text using a specific FIGlet font:
```bash
python main.py -t "Hello" -f banner
```

Send a pre-rendered binary file to the display:
```bash
python main.py -i frame.bin
```

Convert a binary file to hexadecimal (without sending to display):
```bash
python main.py -i frame.bin -o frame.hex -d b h
```

---

## Architecture

```
main.py
├── inout/
│   ├── standard.py   # CLI argument handling, format conversion pipeline
│   ├── serial.py     # Serial port communication
│   └── server.py     # HTTP server mode (partial implementation)
├── frame/
│   ├── control.py    # Builds control frames (display config + animation settings)
│   └── data.py       # Wraps pixel data into protocol frames with checksum
├── view/
│   └── text.py       # Text → figlet → binary bitmap conversion
└── fonts/
    └── banner.flf    # Bundled FIGlet font
```

### Data flow

```
Text input
    → figlet (ASCII art)
    → binary bitmap (# → 1, space → 0)
    → data frame (pixel payload + sign markers)
    → control frame (display config + animation flags)
    → serial port → display
```

---

## Protocol

Each transmission consists of a **1002-byte frame**:

| Bytes | Content |
|---|---|
| 0 | Display number |
| 1 | Sign marker (`0x7f` = first frame, `0x6f`/`0x7e` = middle, etc.) |
| 2–10 | Control metadata (width, height, color, animation config) |
| 11–1000 | Pixel data (990 bytes max) |
| 1001 | Checksum (sum of all bytes mod 256) |

### Transition types

The animation mode byte in the control frame selects the transition:

| Value | Transition |
|---|---|
| `move_right` | Move from right |
| `move_left` | Move from left |
| `scroll_up` | Scroll up |
| `scroll_down` | Scroll down |
| `jump_right` | Jump from right |
| `open_left` | Open from left |
| `open_right` | Open from right |
| `open_bottom` | Open from bottom |
| `open_top` | Open from top |
| `open_center` | Open from center |
| `open_sides` | Open from both sides |
| `cover_center` | Cover from center |
| `cover_sides` | Cover from both sides |
| `immediate` | No transition |
| `random` | Random transition |

### Speed

Four speed levels, from slowest to fastest: **Slow → Median → Fast → Fastest**

### Append mode flags

After the transition, append mode controls how the content behaves on screen:

| Flag | Behavior |
|---|---|
| `flicker` | Content flashes three times after appearing |
| `pause` | Content pauses for a configurable number of seconds |
| `continuum` | Next frame appears immediately as the current one disappears |
| `quiescence` | Content stays on screen until new data is sent (suitable for single-page display) |
| `animation` | Enable animation |
| `continuous` | Loop continuously |
| `winkle` | Winkle effect |
| `time` | Time-based display |
| `repose` | Rest state |

### Text rendering

Text wider than the display is automatically split across multiple screens. Each character block is 8×16 pixels, packed MSB-first into bytes.

---

## License

MIT
