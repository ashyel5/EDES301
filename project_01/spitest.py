import spidev
s = spidev.SpiDev()
s.open(1, 0)
s.mode = 0
s.max_speed_hz = 1000000
print(s.xfer2([0xA5, 0x5A, 0x01]))
