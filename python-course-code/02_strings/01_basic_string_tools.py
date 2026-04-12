# ================================================================================
# STRINGS (BASICS • LENGTH • COUNTING • TYPE CONVERSION)
# ----------------------------------------
# Strings are one of the most used data types in Python.
# They represent text and support many powerful operations.
#
# In this section we cover:
# - Type conversion
# - Length checking
# - Counting substrings
# ================================================================================


# ---------------------------------------
# Type Conversion (Numbers → Strings)
# ---------------------------------------
# We must convert numbers to strings before concatenation.

name = "Baraa"
print(type(name))  # -> <class 'str'>

age = 24
print(type(age))   # -> <class 'int'>

print("Your Age is: " + str(age))
# -> Your Age is: 24

age = age + 5
age = str(age)

print(type(age))  # -> <class 'str'>

# age = age + 5  # ❌ Error (cannot add int to str)


# ---------------------------------------
# String Length
# ---------------------------------------
# len() returns number of characters.

password = "123a58478as"

print(len(password))  # -> 11

if len(password) < 8:
    print("Your Password is too short!")

# ---------------------------------------
# Repeating Strings
# ---------------------------------------
print("ha" * 3)              # ➜ hahaha
print("=" * 30)              # ➜ ==============================

# ---------------------------------------
# Counting Substrings
# ---------------------------------------
# count() checks how many times something appears.
# It is case-sensitive.

text = """
Python is easy to learn.
Python is powerful$.
Many people love python.
"""

print(text.count("Python"))  # -> 2  (case-sensitive)
print(text.count("python"))  # -> 1
print(text.count("$"))       # -> 1


# ---------------------------------------
# Case Sensitivity Awareness
# ---------------------------------------
# Convert to lower() for consistent comparisons.

print(text.lower().count("python")) # -> 3  (after normalizing case)
