import re

# Limits to  Alphanumeric characters, [,.], 5-50 characters in length
regex_note = re.compile(r'^[a-zA-Z0-9,.\x20]{0,256}$')

regex_phone = re.compile(r'^[0-9]{10,}$')
