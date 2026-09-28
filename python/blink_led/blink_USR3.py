# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Blink USR3 LED
--------------------------------------------------------------------------
License:
Copyright 2026 - Asher Yellen

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Blinks the USR3 LED on the PocketBeagle at 5 Hz (5 full on/off cycles per
second) using the Adafruit BBIO library.

Usage:
  python3 blink_USR3.py

Press Ctrl+C to stop the program.  The GPIO is cleaned up on exit.

Timing:
  5 Hz  -->  period = 1 / 5 = 0.2 seconds per full on/off cycle
        -->  0.1 seconds ON + 0.1 seconds OFF

Hardware:
  USR3 is connected to GPIO1_24 (pin GPMC_A8).  The Adafruit BBIO library
  knows this LED by the name "USR3".

--------------------------------------------------------------------------
"""

import time

import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

LED_PIN        = "USR3"                  # Adafruit BBIO name for the USR3 LED
BLINK_FREQ_HZ  = 5                       # Full on/off cycles per second
HALF_PERIOD_S  = 1.0 / (2 * BLINK_FREQ_HZ)   # Time spent ON (or OFF) = 0.1 s

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def setup():
    """ Configure the LED pin as an output. """
    GPIO.setup(LED_PIN, GPIO.OUT)
# End def


def blink_forever():
    """ Blink the LED at BLINK_FREQ_HZ until interrupted (Ctrl+C). """
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)      # LED on
        time.sleep(HALF_PERIOD_S)

        GPIO.output(LED_PIN, GPIO.LOW)       # LED off
        time.sleep(HALF_PERIOD_S)
# End def


def cleanup():
    """ Turn the LED off and release the GPIO. """
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
# End def

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == "__main__":

    setup()

    try:
        blink_forever()
    except KeyboardInterrupt:
        pass

    cleanup()
    print("Program Complete")