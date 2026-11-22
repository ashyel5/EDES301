import time
import Adafruit_BBIO.GPIO as GPIO

CS, SCK, MOSI = "P1_6", "P1_8", "P1_12"
DC, RST, BL = "P2_3", "P2_5", "P2_10"

for p in (CS, SCK, MOSI, DC, RST, BL):
    GPIO.setup(p, GPIO.OUT)

GPIO.output(CS, GPIO.HIGH)
GPIO.output(SCK, GPIO.LOW)
GPIO.output(BL, GPIO.HIGH)

def send_byte(b):
    for i in range(8):
        GPIO.output(MOSI, GPIO.HIGH if b & 0x80 else GPIO.LOW)
        GPIO.output(SCK, GPIO.HIGH)
        GPIO.output(SCK, GPIO.LOW)
        b = (b << 1) & 0xFF

def cmd(c, data=()):
    GPIO.output(DC, GPIO.LOW)
    GPIO.output(CS, GPIO.LOW)
    send_byte(c)
    GPIO.output(DC, GPIO.HIGH)
    for d in data:
        send_byte(d)
    GPIO.output(CS, GPIO.HIGH)

# reset
GPIO.output(RST, GPIO.LOW);  time.sleep(0.1)
GPIO.output(RST, GPIO.HIGH); time.sleep(0.12)

cmd(0x01); time.sleep(0.15)   # software reset
cmd(0x11); time.sleep(0.12)   # sleep out
cmd(0x3A, [0x55])             # 16-bit color
cmd(0x36, [0x48])             # orientation
cmd(0x29)                     # display on

# red 50x50 square in the top-left corner
cmd(0x2A, [0, 0, 0, 49])
cmd(0x2B, [0, 0, 0, 49])
GPIO.output(DC, GPIO.LOW)
GPIO.output(CS, GPIO.LOW)
send_byte(0x2C)
GPIO.output(DC, GPIO.HIGH)
for i in range(50 * 50):
    send_byte(0xF8)
    send_byte(0x00)
GPIO.output(CS, GPIO.HIGH)
print("done")