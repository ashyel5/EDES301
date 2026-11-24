"""main.py -- entry point for the whole Morse project (this is what autoboot runs)."""

import config
from button import Button
from indicator import Indicator
from morse_key import MorseKey
from display import Display
from training_mode import MorseTrainer


def main():
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


if __name__ == "__main__":
    main()