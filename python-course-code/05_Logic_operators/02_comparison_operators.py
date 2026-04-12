# ================================================================================
# COMPARISON OPERATORS
# ----------------------------------------
# Comparison operators are used to compare values and return Boolean results.
# These include equality, inequality, greater/less than, and range comparisons.
# ================================================================================

# ---------------------------------------
# Basic Comparison Operators
# ---------------------------------------
print(10 == 10)   # ➜ True  (equal to)
print(10 != 10)   # ➜ False (not equal to)
print(7 > 3)      # ➜ True  (greater than)
print(7 >= 3)     # ➜ True  (greater than or equal to)
print(3 < 7)      # ➜ True  (less than)
print(7 <= 7)     # ➜ True  (less than or equal to)

# ---------------------------------------
# String Comparison: Case Sensitivity
# ---------------------------------------
print("a" == "A")                     # ➜ False (case-sensitive)
print("a".lower() == "A".lower())     # ➜ True  (case-insensitive comparison)

# ---------------------------------------
# Alphabetical Comparison
# ---------------------------------------
print("a" < "b")  # ➜ True — "a" comes before "b" in ASCII order

# ---------------------------------------
# Common Mistake: Using = Instead of ==
# ---------------------------------------
# print("a" = "A")  # SyntaxError: cannot use = in comparisons
# Correct usage:
print("a" == "A")  # ➜ False

# ---------------------------------------
# Assignment vs Comparison
# ---------------------------------------
x = "a"            # Assignment
print(x == "a")    # ➜ True  (comparison)

# ---------------------------------------
# Chained Comparison (Range Check)
# ---------------------------------------
age = 18
print(18 <= age <= 30)  # ➜ True (age is between 18 and 30)

age = 35
print(18 <= age <= 30)  # ➜ False (35 is outside the range)
