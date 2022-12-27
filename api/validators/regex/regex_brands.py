import re

# Limits to  Alphanumeric characters, 4 characters in length
brands_name_regex = re.compile(r'^[A-Z0-9]{4,4}$')