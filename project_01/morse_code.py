"""Pure Python lookup/translation. No hardware, so it runs on any computer."""

MORSE = {
    "A": ".-",   "B": "-...", "C": "-.-.", "D": "-..",  "E": ".",
    "F": "..-.", "G": "--.",  "H": "....", "I": "..",   "J": ".---",
    "K": "-.-",  "L": ".-..", "M": "--",   "N": "-.",   "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.",  "S": "...",  "T": "-",
    "U": "..-",  "V": "...-", "W": ".--",  "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}
REVERSE = {pattern: char for char, pattern in MORSE.items()}


def decode_pattern(pattern):
    """'.-' -> 'A'. Returns '?' for an unknown pattern."""
    return REVERSE.get(pattern, "?")


def encode_char(char):
    """'A' -> '.-'. Returns '' for unsupported characters."""
    return MORSE.get(char.upper(), "")


def encode_text(text):
    """'SOS HI' -> '... --- ... / .... ..'"""
    words = [" ".join(encode_char(c) for c in word if encode_char(c))
             for word in text.split()]
    return " / ".join(words)
