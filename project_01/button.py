import time
import Adafruit_BBIO.GPIO as GPIO
import config


class Button:
    def __init__(self, pin, active_high=config.BUTTON_ACTIVE_HIGH):
        self.pin = pin
        self.active_high = active_high
        GPIO.setup(self.pin, GPIO.IN)

    def _raw_pressed(self):
        value = GPIO.input(self.pin)
        return bool(value) == self.active_high

    def is_pressed(self):
        """Debounced read: state must hold for DEBOUNCE_S."""
        first = self._raw_pressed()
        time.sleep(config.DEBOUNCE_S)
        return first if first == self._raw_pressed() else False

    def wait_for_press(self, timeout=None):
        """Block until pressed. Returns True, or False if timeout hit."""
        start = time.time()
        while not self.is_pressed():
            if timeout is not None and time.time() - start >= timeout:
                return False
            time.sleep(0.005)
        return True

    def wait_for_release(self):
        while self.is_pressed():
            time.sleep(0.005)
