import config
from button import Button

buttons = {
    "blue": Button(config.BLUE_BUTTON_PIN),
    "red": Button(config.RED_BUTTON_PIN),
    "green": Button(config.GREEN_BUTTON_PIN),
}
was_pressed = {name: False for name in buttons}

print("Press each button. Ctrl-C to quit.")
try:
    while True:
        for name, button in buttons.items():
            now = button.is_pressed()
            if now and not was_pressed[name]:
                print(name, "pressed")
            elif not now and was_pressed[name]:
                print(name, "released")
            was_pressed[name] = now
except KeyboardInterrupt:
    pass