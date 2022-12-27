import re

# Limits
inv_last_brews_regex = re.compile(r'^[A-Z0-9]{4,4} [0-9]{5,5}$')


# Limits
inv_hop_lot_regex = re.compile(r'^[a-z0-9]{4,50}$')
