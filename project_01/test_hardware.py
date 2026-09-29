"""Run on the PocketBeagle: python3 test_hardware.py"""
import time
import config
from button import Button
from indicator import Indicator
from morse_key import MorseKey
from morse_code import decode_pattern


def main():
    indicator = Indicator()
    key = MorseKey(Button(config.BLUE_BUTTON_PIN), indicator)
    print("Buzzer enabled:", indicator.buzzer_enabled)
    indicator.beep(0.2)
    print("Tap Morse on the blue button. Ctrl-C to quit.")
    try:
        while True:
            pattern = key.read_pattern()
            print(pattern, "->", decode_pattern(pattern))
    except KeyboardInterrupt:
        pass
    finally:
        indicator.cleanup()


if __name__ == "__main__":
    main()
