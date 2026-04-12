# ================================================================================
# LOGICAL OPERATORS & IDENTITY CHECKS
# ----------------------------------------
# Python provides logical operators to combine multiple conditions:
# `and`, `or`, `not` — which return Boolean results based on truth tables.
# This section also covers `in`, `not in`, `is`, and `is not`.
# ================================================================================

# ---------------------------------------
# Basic Logical Operators: and / or
# ---------------------------------------
print(3 > 1 and 5 < 1)   # ➜ False: first is True, second is False
print(3 > 1 and 5 > 1)   # ➜ True: both are True

print(3 > 1 or 5 < 1)    # ➜ True: first is True, second is False
print(3 > 1 or 5 > 1)    # ➜ True: both are True

# ---------------------------------------
# Real-World Example: System Monitoring
# ---------------------------------------
cpu_usage    = 70
memory_usage = 90

print(cpu_usage > 90 or memory_usage > 90)  # ➜ False: both values are within limits

# ---------------------------------------
# Login Validation
# ---------------------------------------
email    = True
password = False

print(email and password)  # ➜ False: both must be True to allow login

# ---------------------------------------
# Logical NOT
# ---------------------------------------
print(not 3 > 2)       # ➜ False
print(not True)        # ➜ False
print(not False)       # ➜ True
print(not not False)   # ➜ False

name = ""
print(not name)        # ➜ True: empty string is falsy
print(not 10)          # ➜ False: 10 is truthy

# ---------------------------------------
# Complex Access Control Logic
# ---------------------------------------
# Allow access if the user is logged in OR a guest,
# BUT they must not be banned.

is_logged_in = True
is_guest     = False
is_banned    = True

print(is_logged_in or is_guest and not is_banned)      # ➜ True (wrong logic)
print((is_logged_in or is_guest) and not is_banned)    # ➜ False (correct logic)

# ---------------------------------------
# Python Challenges
# ---------------------------------------
# 1. Name is not empty and age is >= 18
# 2. Password is at least 8 chars and has no spaces
# 3. Email is not empty, contains '@', and ends with '.com'
# 4. Username is a string, not None, and longer than 5 characters
# 5. User is admin or moderator, and not banned or email verified

# ---------------------------------------
# Membership Operators: in / not in
# ---------------------------------------
print("f" not in "python")      # ➜ True
print(3 not in [1, 2, 3])       # ➜ False

domain = "spam.com"
banned_domains = ["spam.com", "fake.org", "bot.net"]
print(domain not in banned_domains)  # ➜ False

# ---------------------------------------
# Identity Operators: is / is not
# ---------------------------------------
x = ['a', 'b', 'c']
y = ['a', 'b', 'c']

print(x == y)  # ➜ True: same content
print(x is y)  # ➜ False: different objects in memory

x = 10
y = 10

print(x == y)  # ➜ True: same value
print(x is y)  # ➜ True: same object (small integers are cached)

x = ['a', 'b', 'c']
y = x

print(x == y)  # ➜ True: same values
print(x is y)  # ➜ True: same object (same memory reference)

# ---------------------------------------
# Validate Email Exists and Is Not Empty
# ---------------------------------------
email = "b@gmail.com"
print(email != "")              # ➜ True

email = None
print(email is not None and email != "")  # ➜ False
