import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import config


class Indicator:
    """LED + piezo buzzer. The buzzer can be muted with buzzer_enabled=False.

    The buzzer's PWM is started once (silent, 0% duty) and then switched on
    and off by changing the duty cycle. Starting/stopping PWM for every beep
    is slow on the PocketBeagle and was throwing off the key timing.
    """

    def __init__(self, led_pin=config.LED_PIN, buzzer_pin=config.BUZZER_PIN,
                 buzzer_enabled=config.BUZZER_ENABLED):
        self.led_pin = led_pin
        self.buzzer_pin = buzzer_pin
        self.buzzer_enabled = buzzer_enabled

        GPIO.setup(self.led_pin, GPIO.OUT)
        self._set_led(False)

        if self.buzzer_enabled:
            PWM.start(self.buzzer_pin, 0, config.BUZZER_FREQ_HZ)

    def _set_led(self, lit):
        """lit=True means the LED should be visibly on, whatever the wiring."""
        level = GPIO.HIGH if lit == config.LED_ACTIVE_HIGH else GPIO.LOW
        GPIO.output(self.led_pin, level)

    def on(self):
        self._set_led(True)
        if self.buzzer_enabled:
            PWM.set_duty_cycle(self.buzzer_pin, config.BUZZER_DUTY)

    def off(self):
        self._set_led(False)
        if self.buzzer_enabled:
            PWM.set_duty_cycle(self.buzzer_pin, 0)

    def beep(self, seconds):
        self.on()
        time.sleep(seconds)
        self.off()

    def cleanup(self):
        self.off()
        if self.buzzer_enabled:
            PWM.stop(self.buzzer_pin)
        PWM.cleanup()

    def play_morse(self, pattern, unit=config.MORSE_UNIT_SECONDS):
        """Play a pattern like '.-' (dot = 1 unit, dash = 3, 1-unit gap between symbols)."""
        try:
            for i, symbol in enumerate(pattern):
                if symbol == ".":
                    self.beep(unit)
                elif symbol == "-":
                    self.beep(3 * unit)
                else:
                    continue
                if i < len(pattern) - 1:
                    time.sleep(unit)
        finally:
            self.off()