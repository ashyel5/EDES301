"""
training_mode.py -- terminal stand-in for the Morse trainer.

Flow: mode select -> show letter -> flash/buzz its Morse -> user keys it in
-> correct = next letter, wrong = replay and retry.

The ONLY things you should need to touch are the three adapter functions
marked "ADAPT ME" -- they wrap your existing MorseCode / Indicator / MorseKey
classes. Everything else is independent of your hardware classes.
"""

import time
import random
import config
from button import Button
from indicator import Indicator
from morse_key import MorseKey
import morse_code



# ---------------------------------------------------------------------------
# ADAPT ME: three thin wrappers around your real code
# ---------------------------------------------------------------------------
def letter_to_morse(letter):
    """'A' -> '.-'   (swap in whatever your MorseCode class calls this)"""
    return morse_code.encode_char(letter)


def play_morse(indicator, morse):
    """Flash LED + buzz the pattern, e.g. '.-' """
    indicator.play_morse(morse)


def read_letter(key):
    """Block until the user keys in one letter; return it as 'A'-'Z',
    or None if the pattern didn't decode to anything."""
    pattern = key.read_pattern()
    if pattern is None:
        return None

    return morse_code.decode_pattern(pattern)


# ---------------------------------------------------------------------------
# Display stand-in. When the TFT arrives, write a Display class with the same
# three methods and pass it in instead -- TrainingMode won't change.
# ---------------------------------------------------------------------------
class TerminalDisplay:
    def show_menu(self, options, selected):
        print("\n=== MORSE TRAINER ===")
        for i, (name, enabled) in enumerate(options):
            cursor = ">" if i == selected else " "
            tag = "" if enabled else "  (coming soon)"
            print(f" {cursor} {i + 1}) {name}{tag}")

    def show_letter(self, letter, morse):
        print(f"\n  Letter:  {letter}     Morse:  {morse}")

    def show_message(self, text):
        print(f"  {text}")


# ---------------------------------------------------------------------------
# Training mode
# ---------------------------------------------------------------------------
class TrainingMode:
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, display, indicator, key, shuffle=False):
        self.display = display
        self.indicator = indicator
        self.key = key
        self.shuffle = shuffle

    def run(self):
        letters = list(self.LETTERS)
        if self.shuffle:
            random.shuffle(letters)

        self.display.show_message("Training mode -- Ctrl+C to quit")
        total_attempts = 0

        try:
            for letter in letters:
                total_attempts += self._drill_letter(letter)
        except KeyboardInterrupt:
            self.display.show_message("\nExiting training mode.")
            return

        self.display.show_message(
            f"\nAll done! {len(letters)} letters in {total_attempts} attempts."
        )

    def _drill_letter(self, letter):
        """Show/play a letter until the user keys it correctly.
        Returns the number of attempts it took."""
        morse = letter_to_morse(letter)
        attempts = 0

        self.display.show_letter(letter, morse)
        play_morse(self.indicator, morse)

        while True:
            attempts += 1
            self.display.show_message("Your turn...")
            answer = read_letter(self.key)

            if answer == letter:
                self.display.show_message("Correct!")
                time.sleep(0.6)
                return attempts

            shown = answer if answer else "?"
            self.display.show_message(f"Not quite (got {shown}). Watch again:")
            time.sleep(0.5)
            play_morse(self.indicator, morse)


# ---------------------------------------------------------------------------
# Start-screen controller (terminal menu for now)
# ---------------------------------------------------------------------------
class MorseTrainer:
    def __init__(self, display, indicator, key, green_button, red_button):
        self.display = display
        self.indicator = indicator
        self.key = key
        self.green = green_button
        self.red = red_button
        # (name, enabled, button color)
        self.options = [("Training", True, "green"), ("Typing", False, "red")]

    def run(self):
        while True:
            self.display.show_menu(self.options, None)
            if self._wait_for_choice() == "green":
                TrainingMode(self.display, self.indicator, self.key).run()
                time.sleep(2)           # let the last message stay up
            else:
                self.display.show_message("Typing mode coming soon")
                time.sleep(1.5)

    def _wait_for_choice(self):
        """Block until green or red is pressed; returns 'green' or 'red'."""
        while True:
            if self.green.is_pressed():
                self._wait_for_release(self.green)
                return "green"
            if self.red.is_pressed():
                self._wait_for_release(self.red)
                return "red"
            time.sleep(0.02)

    @staticmethod
    def _wait_for_release(button):
        while button.is_pressed():
            time.sleep(0.02)
        time.sleep(0.05)                # debounce


if __name__ == "__main__":
    from display import Display
    indicator = Indicator()
    key = MorseKey(Button(config.BLUE_BUTTON_PIN), indicator)
    green = Button(config.GREEN_BUTTON_PIN)
    red = Button(config.RED_BUTTON_PIN)
    display = Display()
    try:
        MorseTrainer(display, indicator, key, green, red).run()
    except KeyboardInterrupt:
        pass
    finally:
        display.close()
        indicator.cleanup()