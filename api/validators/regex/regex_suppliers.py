import re

# Limits to  Alphanumeric characters, 5-50 characters in length
supplier_name_regex = re.compile(r'^[a-zA-Z0-9\x20]{5,50}$')