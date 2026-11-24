"""
display.py -- ILI9341 240x320 SPI TFT for the Morse trainer.

Same three methods as TerminalDisplay in training_mode.py (show_menu,
show_letter, show_message), so TrainingMode doesn't need to change.

Needs Pillow and a font:
    sudo apt install python3-pil fonts-dejavu-core
Run the same config-pin commands you used for display_test.py first.
"""

import time

import spidev
import Adafruit_BBIO.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 240, 320
DC, RST, BL = "P2_3", "P2_5", "P2_10"
BUS, DEV = 0, 0
SPI_SPEED_HZ = 8000000      # drop to 1000000 if the picture looks garbled
FLIP_180 = True             # True = rotate the picture 180 degrees

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Everything is drawn with palette indices, then converted to RGB565 in one
# fast step (see _to_rgb565). Add a color here to get a new index.
BG, WHITE, DOT, DASH, GRAY, HILITE = range(6)
COLORS = [
    (10, 10, 30),       # BG
    (255, 255, 255),    # WHITE  (the letter)
    (0, 200, 255),      # DOT
    (255, 170, 0),      # DASH
    (170, 170, 170),    # GRAY   (messages)
    (50, 50, 110),      # HILITE (selected menu row)
]
PALETTE = [c for rgb in COLORS for c in rgb]
PALETTE += [0] * (768 - len(PALETTE))


def _build_tables():
    """Two 256-byte lookup tables: palette index -> RGB565 high/low byte."""
    hi, lo = bytearray(256), bytearray(256)
    for i, (r, g, b) in enumerate(COLORS):
        pixel = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        hi[i] = pixel >> 8
        lo[i] = pixel & 0xFF
    return bytes(hi), bytes(lo)


HI_TABLE, LO_TABLE = _build_tables()


class Display:
    def __init__(self):
        GPIO.setup(DC, GPIO.OUT)
        GPIO.setup(RST, GPIO.OUT)
        GPIO.setup(BL, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(BUS, DEV)
        self.spi.mode = 0
        self.spi.max_speed_hz = SPI_SPEED_HZ

        self._fonts = {}
        self._shown = None      # what is on screen now; skips identical redraws
        self._letter = None
        self._morse = ""
        self._message = ""

        GPIO.output(BL, GPIO.HIGH)
        self._init_panel()

    # ------------------------------------------------------------------
    # Public API (matches TerminalDisplay)
    # ------------------------------------------------------------------
    def show_letter(self, letter, morse):
        """Big letter on top, its dots and dashes underneath."""
        self._letter, self._morse, self._message = letter, morse, ""
        self._refresh(("letter", letter, morse, ""))

    def show_message(self, text):
        """Small status text at the bottom (or centered if no letter yet)."""
        self._message = text.strip()
        self._refresh(("letter", self._letter, self._morse, self._message))

    def show_menu(self, options, selected):
        """options is a list of (name, enabled)."""
        self._letter, self._morse, self._message = None, "", ""
        self._refresh(("menu", tuple(options), selected))

    def close(self):
        self.spi.close()

    # ------------------------------------------------------------------
    # Screens
    # ------------------------------------------------------------------
    def _refresh(self, state):
        if state == self._shown:
            return
        img = Image.new("P", (WIDTH, HEIGHT), BG)
        img.putpalette(PALETTE)
        draw = ImageDraw.Draw(img)

        if state[0] == "menu":
            self._draw_menu(draw, state[1], state[2])
        else:
            self._draw_letter_screen(draw, state[1], state[2], state[3])

        self._push(img)
        self._shown = state

    def _draw_letter_screen(self, draw, letter, morse, message):
        if letter:
            self._text(draw, letter, 170, WIDTH // 2, 105, WHITE)
            self._draw_morse(draw, morse, 220)

        if message:
            font = self._font(16)
            lines = self._wrap(draw, message, font, WIDTH - 20)[:2]
            top = 270 if letter else HEIGHT // 2 - 10 * len(lines)
            for i, line in enumerate(lines):
                self._text(draw, line, 16, WIDTH // 2, top + 20 * i + 10, GRAY)

    def _draw_menu(self, draw, options, selected):
        self._text(draw, "MORSE TRAINER", 22, WIDTH // 2, 40, WHITE)
        for i, (name, enabled) in enumerate(options):
            y = 100 + i * 50
            if i == selected:
                draw.rectangle([10, y, WIDTH - 11, y + 38], fill=HILITE)
            label = name if enabled else name + " (soon)"
            self._text(draw, label, 17, 16, y + 19,
                       WHITE if enabled else GRAY, align="left")

    def _draw_morse(self, draw, morse, cy):
        """Dot = 1 unit, dash = 3 units, gap = 1 unit (real Morse timing)."""
        if not morse:
            return
        units = sum(1 if s == "." else 3 for s in morse) + (len(morse) - 1)
        u = min(24, (WIDTH - 20) // units)      # shrink to fit long codes
        x = (WIDTH - units * u) // 2
        y = cy - u // 2
        for s in morse:
            if s == ".":
                draw.ellipse([x, y, x + u - 1, y + u - 1], fill=DOT)
                x += 2 * u
            else:
                self._pill(draw, x, y, 3 * u, u, DASH)
                x += 4 * u

    @staticmethod
    def _pill(draw, x, y, w, h, fill):
        draw.ellipse([x, y, x + h - 1, y + h - 1], fill=fill)
        draw.ellipse([x + w - h, y, x + w - 1, y + h - 1], fill=fill)
        draw.rectangle([x + h // 2, y, x + w - h // 2 - 1, y + h - 1],
                       fill=fill)

    # ------------------------------------------------------------------
    # Text helpers
    # ------------------------------------------------------------------
    def _font(self, size):
        if size not in self._fonts:
            try:
                self._fonts[size] = ImageFont.truetype(FONT_PATH, size)
            except (IOError, OSError):
                # tiny fallback: install fonts-dejavu-core for the real one
                self._fonts[size] = ImageFont.load_default()
        return self._fonts[size]

    @staticmethod
    def _measure(draw, text, font):
        """Returns (width, height, left offset, top offset)."""
        if hasattr(draw, "textbbox"):               # newer Pillow
            l, t, r, b = draw.textbbox((0, 0), text, font=font)
            return r - l, b - t, l, t
        w, h = draw.textsize(text, font=font)       # older Pillow
        return w, h, 0, 0

    def _text(self, draw, text, size, x, cy, fill, align="center"):
        """Draw text vertically centered on cy. x is the center, or the
        left edge when align="left"."""
        font = self._font(size)
        w, h, l, t = self._measure(draw, text, font)
        left = x - w // 2 if align == "center" else x
        draw.text((left - l, cy - h // 2 - t), text, font=font, fill=fill)

    def _wrap(self, draw, text, font, max_w):
        lines, line = [], ""
        for word in text.split():
            trial = (line + " " + word).strip()
            if line and self._measure(draw, trial, font)[0] > max_w:
                lines.append(line)
                line = word
            else:
                line = trial
        if line:
            lines.append(line)
        return lines

    # ------------------------------------------------------------------
    # Panel / SPI
    # ------------------------------------------------------------------
    def _init_panel(self):
        GPIO.output(RST, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(RST, GPIO.HIGH)
        time.sleep(0.12)

        self._command(0x01)
        time.sleep(0.15)                    # software reset
        self._command(0x11)
        time.sleep(0.12)                    # sleep out
        self._command(0x3A, [0x55])         # 16-bit RGB565
        # orientation / color order: 0x48 normal, 0x88 = rotated 180 degrees
        self._command(0x36, [0x88 if FLIP_180 else 0x48])
        self._command(0x29)                 # display on

    def _command(self, c, data=None):
        GPIO.output(DC, GPIO.LOW)
        self.spi.writebytes([c])
        if data:
            GPIO.output(DC, GPIO.HIGH)
            self._write(data)

    def _write(self, data):
        data = bytes(data)
        for i in range(0, len(data), 4096):         # spidev buffer limit
            self.spi.writebytes(list(data[i:i + 4096]))

    @staticmethod
    def _to_rgb565(img):
        """Palette image -> RGB565 bytes using two lookup tables (all in C,
        so a full frame takes milliseconds instead of a slow pixel loop)."""
        idx = img.tobytes()
        out = bytearray(len(idx) * 2)
        out[0::2] = idx.translate(HI_TABLE)
        out[1::2] = idx.translate(LO_TABLE)
        return out

    def _push(self, img):
        self._command(0x2A, [0, 0, (WIDTH - 1) >> 8, (WIDTH - 1) & 0xFF])
        self._command(0x2B, [0, 0, (HEIGHT - 1) >> 8, (HEIGHT - 1) & 0xFF])
        self._command(0x2C)
        GPIO.output(DC, GPIO.HIGH)
        self._write(self._to_rgb565(img))
