import re

# Limits to  Alphanumeric characters, 5-50 characters in length, no spaces
regex_users_name = re.compile(r'^[a-zA-Z0-9]{3,50}$')


# Limits to  Alphanumeric characters, 5-8 characters in length, no spaces
regex_users_eid = re.compile(r'^[a-zA-Z0-9]{5,8}$')


# Limits to 8 characters minimun, Uppercase, Lowercase, Number, Special Character [#?!@$%^&*-]
regex_users_password = re.compile(r"""^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!"#$%&'()*+,-\/.:;<=>?@[\]^_`{|}~\\]).{8,}$""")
# regex_users_password = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
