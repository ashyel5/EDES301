import Adafruit_BBIO.GPIO as GPIO

for name in ["P1_06", "P1_6", "P1_08", "P1_8", "P1_12",
             "P2_3", "P2_5", "P2_10"]:
    try:
        GPIO.setup(name, GPIO.OUT)
        print(name, "OK")
    except Exception as e:
        print(name, "FAILED:", e)