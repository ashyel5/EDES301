import time
import spidev
import Adafruit_BBIO.GPIO as GPIO

DC, RST, BL = "P2_3", "P2_5", "P2_10"
BUS, DEV = 0, 0            # match your /dev/spidevX.Y

GPIO.setup(DC, GPIO.OUT)
GPIO.setup(RST, GPIO.OUT)
GPIO.setup(BL, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(BUS, DEV)
spi.mode = 0
spi.max_speed_hz = 1000000

def write(data):
    for i in range(0, len(data), 4096):   # spidev buffer limit
        spi.writebytes(data[i:i + 4096])

def cmd(c, data=None):
    GPIO.output(DC, GPIO.LOW)
    spi.writebytes([c])
    if data:
        GPIO.output(DC, GPIO.HIGH)
        write(data)

GPIO.output(BL, GPIO.HIGH)
GPIO.output(RST, GPIO.LOW); time.sleep(0.1)
GPIO.output(RST, GPIO.HIGH); time.sleep(0.12)

cmd(0x01); time.sleep(0.15)        # software reset
cmd(0x11); time.sleep(0.12)        # sleep out
cmd(0x3A, [0x55])                  # 16-bit RGB565
cmd(0x36, [0x48])                  # orientation / color order
cmd(0x29)                          # display on

cmd(0x2A, [0, 0, 0, 239])          # column range 0-239
cmd(0x2B, [0, 0, 0x01, 0x3F])      # row range 0-319
cmd(0x2C)                          # start pixel write
GPIO.output(DC, GPIO.HIGH)
write([0xF8, 0x00] * (240 * 320))  # RGB565 red

spi.close()

