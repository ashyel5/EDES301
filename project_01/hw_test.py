import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

# Swap these if a button is mapped differently than you expect
RED_BTN   = "P2_2"
GREEN_BTN = "P2_4"
KEY_BTN   = "P2_6"
LED       = "P2_8"
BUZZER    = "P2_1"

# Each button plays its own tone while held
TONES = {RED_BTN: 440, GREEN_BTN: 880, KEY_BTN: 660}

def pressed(pin):
    return GPIO.input(pin) == 0   # active low

def main():
    for pin in TONES:
        GPIO.setup(pin, GPIO.IN)
    GPIO.setup(LED, GPIO.OUT)

    current_tone = None
    print("Hold a button: LED on + tone. Ctrl-C to quit.")
    try:
        while True:
            tone = None
            for pin, freq in TONES.items():
                if pressed(pin):
                    tone = freq
                    break

            if tone != current_tone:
                if tone is None:
                    PWM.stop(BUZZER)
                    GPIO.output(LED, GPIO.LOW)
                else:
                    if current_tone is not None:
                        PWM.stop(BUZZER)
                    PWM.start(BUZZER, 50, tone)
                    GPIO.output(LED, GPIO.HIGH)
                current_tone = tone

            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        PWM.stop(BUZZER)
        PWM.cleanup()
        GPIO.output(LED, GPIO.LOW)
        GPIO.cleanup()
        print("Done")

if __name__ == "__main__":
    main()
