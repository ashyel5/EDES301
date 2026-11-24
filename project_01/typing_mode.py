import time

import config
from morse_code import decode_pattern


class TypingMode:
    """Blue = Morse key, red = delete last letter, green = done."""

    def __init__(self, key, red_button, green_button, display):
        self.key = key
        self.red = red_button
        self.green = green_button
        self.display = display

    def run(self):
        text = ""
        last_letter_time = None     # when the last letter was committed

        # ignore the red press that brought us into this mode
        self.red.wait_for_release()
        self.green.wait_for_release()
        self.display.show_typing(text)

        while True:
            # Wait briefly for a letter; returns None if blue wasn't pressed.
            # If blue IS pressed, this collects the whole letter.
            pattern = self.key.read_pattern(first_timeout=0.05)
            if pattern:
                text += decode_pattern(pattern)
                last_letter_time = time.time()
                self.display.show_typing(text)

            if self.red.wait_for_press(0.02):
                self.red.wait_for_release()
                text = text[:-1]
                last_letter_time = None
                self.display.show_typing(text)

            if self.green.wait_for_press(0.02):
                self.green.wait_for_release()
                return text

            # read_pattern already waited LETTER_GAP_S, so only the extra
            # silence counts toward a space
            if (last_letter_time and text and not text.endswith(" ")
                    and time.time() - last_letter_time
                    >= config.WORD_GAP_S - config.LETTER_GAP_S):
                text += " "
                last_letter_time = None
                self.display.show_typing(text)