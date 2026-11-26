"""Try the TFT display on its own, before wiring it into training mode."""

import time

import morse_code
from display import Display

display = Display()
try:
    display.show_menu([("Training mode", True), ("Typing mode", False)], 0)
    time.sleep(2)

    for letter in "AEQ5":                   # short, medium and long codes
        display.show_letter(letter, morse_code.encode_char(letter))
        time.sleep(2)

    display.show_message("Your turn...")
    time.sleep(2)
    display.show_message("Not quite (got T). Watch again:")
    time.sleep(2)
finally:
    display.close()
