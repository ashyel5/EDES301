"""No hardware needed: python3 test_morse_code.py"""
from morse_code import decode_pattern, encode_char, encode_text

assert decode_pattern(".-") == "A"
assert decode_pattern("...") == "S"
assert decode_pattern("......") == "?"
assert encode_char("s") == "..."
assert encode_text("SOS") == "... --- ..."
assert encode_text("HI YOU") == ".... .. / -.-- --- ..-"
print("All MorseCode tests passed")
