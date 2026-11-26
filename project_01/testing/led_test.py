import time
import Adafruit_BBIO.GPIO as GPIO
import config

GPIO.setup(config.LED_PIN, GPIO.OUT)

GPIO.output(config.LED_PIN, GPIO.HIGH)
print("HIGH for 5 seconds")
time.sleep(5)

GPIO.output(config.LED_PIN, GPIO.LOW)
print("LOW for 5 seconds")
time.sleep(5)