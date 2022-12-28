import re

# Limits to  Alphanumeric characters, 5-50 characters in length, no spaces
regex_jobs_jobname = re.compile(r'^[a-zA-Z0-9\x20]{5,50}$')

# Limits to
regex_jobs_jobarea = re.compile(r'\b(Brewhouse|Finishing)\b')