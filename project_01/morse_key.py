import time
import config


class MorseKey:
    """Turns presses of one Button into Morse symbols and letters."""

    def __init__(self, button, indicator=None):
        self.button = button
        self.indicator = indicator  # optional: LED/buzzer follow the key

    def read_symbol(self, timeout=None):
        """Wait for one press. Returns '.', '-', or None if timeout hit."""
        if not self.button.wait_for_press(timeout):
            return None
        start = time.time()
        if self.indicator:
            self.indicator.on()
        self.button.wait_for_release()
        held = time.time() - start          # measure before anything slow
        if self.indicator:
            self.indicator.off()
        return "-" if held >= config.DASH_MIN_S else "."

    def read_pattern(self, first_timeout=None):
        """Collect symbols until a letter-length silence. Returns e.g. '.-',
        or None if nothing was pressed within first_timeout."""
        symbol = self.read_symbol(first_timeout)
        if symbol is None:
            return None
        pattern = symbol
        while True:
            symbol = self.read_symbol(timeout=config.LETTER_GAP_S)
            if symbol is None:
                return pattern
            pattern += symbol
