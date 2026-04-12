# ================================================================================
# ABSOLUTE VALUE & ROUNDING FUNCTIONS
# ----------------------------------------
# Python provides built-in tools to:
# - Remove negative signs
# - Round numbers
# - Control decimal precision
#
# These are extremely common in financial,
# analytics, and data processing tasks.
# ================================================================================


# ---------------------------------------
# Absolute Value
# ---------------------------------------
# abs() removes the negative sign.
# It always returns a positive number.

print(abs(2 - 10))   # -> 8

# ---------------------------------------
# Rounding Numbers
# ---------------------------------------
# round() rounds to nearest value.
# You can control decimal places.

price = 35.54879865

print(round(price))      # -> 36    (nearest whole number)
print(round(price, 2))   # -> 35.55 (2 decimal places)
print(round(price, 1))   # -> 35.5  (1 decimal place)

# ---------------------------------------
# Math Module (Advanced Rounding Control)
# ---------------------------------------
# The math module provides more specific control.

import math

print(math.floor(price))  # -> 35 (always round down)
print(math.ceil(price))   # -> 36 (always round up)
print(math.trunc(price))  # -> 35 (remove decimal part)

print(int(price))         # -> 35 (similar to trunc)
