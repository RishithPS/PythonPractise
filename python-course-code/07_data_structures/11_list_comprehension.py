# ================================================================================
# LIST COMPREHENSIONS
# ----------------------------------------
# List comprehension allows us to create lists
# in a clean and compact way.
#
# It combines:
# - Iteration
# - Optional filtering
# - Optional transformation
# In a single readable expression.
# ================================================================================



# Task:
# 1. Keep only valid domains (must contain a dot)
# 2. Convert everything to lowercase

domains = [
    'www.google.com',
    'openai.com',
    'localhost',
    'WWW.DATAWITHBARAA.COM'
]
# one line -> cleaned = [d.lower() for d in domains if '.' in d] 

cleaned = [
    d.lower()
    for d in domains
    if '.' in d
]

print(cleaned)
