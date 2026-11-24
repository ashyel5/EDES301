"""Central settings. Change things here, not in the classes."""

# --- Quiet mode: set to False when testing in the library ---
BUZZER_ENABLED = True

# --- Pins (Adafruit_BBIO names). TODO: replace with the pins you actually wired ---
RED_BUTTON_PIN = "P2_2"      # 
GREEN_BUTTON_PIN = "P2_4"    # 
BLUE_BUTTON_PIN = "P2_6"
LED_PIN = "P2_8"
BUZZER_PIN = "P2_1"         # must be a PWM-capable pin (e.g. P1_36, P1_33, P2_1, P2_3)

# --- Button wiring ---
BUTTON_ACTIVE_HIGH = False    # True: pin reads 1 when pressed. False: reads 0 when pressed
DEBOUNCE_S = 0.02

# --- LED wiring ---
# True:  pin HIGH lights the LED (pin -> resistor -> LED -> ground)
# False: pin LOW lights the LED (3.3V -> resistor -> LED -> pin)
LED_ACTIVE_HIGH = True


# --- Buzzer ---
BUZZER_FREQ_HZ = 600
BUZZER_DUTY = 10

# --- Morse timing (seconds) ---
DASH_MIN_S = 0.25            # press shorter than this = dot, longer = dash
LETTER_GAP_S = 0.75          # silence this long ends a letter
WORD_GAP_S = 1.75            # silence this long ends a word
MORSE_UNIT_SECONDS = 0.2
