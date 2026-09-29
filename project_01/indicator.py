import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import config


class Indicator:
    """LED + piezo buzzer. The buzzer can be muted with buzzer_enabled=False."""

    def __init__(self, led_pin=config.LED_PIN, buzzer_pin=config.BUZZER_PIN,
                 buzzer_enabled=config.BUZZER_ENABLED):
        self.led_pin = led_pin
        self.buzzer_pin = buzzer_pin
        self.buzzer_enabled = buzzer_enabled
        self._buzzer_running = False

        GPIO.setup(self.led_pin, GPIO.OUT)
        self._set_led(False)
    
    def _set_led(self, lit):
        """lit=True means the LED should be visibly on, whatever the wiring."""
        level = GPIO.HIGH if lit == config.LED_ACTIVE_HIGH else GPIO.LOW
        GPIO.output(self.led_pin, level)
        
    def on(self):
        self._set_led(True)
        if self.buzzer_enabled and not self._buzzer_running:
            PWM.start(self.buzzer_pin, config.BUZZER_DUTY, config.BUZZER_FREQ_HZ)
            self._buzzer_running = True

    def off(self):
        self._set_led(False)
        if self._buzzer_running:
            PWM.stop(self.buzzer_pin)
            self._buzzer_running = False

    def beep(self, seconds):
        self.on()
        time.sleep(seconds)
        self.off()

    def cleanup(self):
        self.off()
        PWM.cleanup()
