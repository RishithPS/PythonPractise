# ================================================================================
# DATA TYPES
# ----------------------------------------
# Python has multiple built-in data types to represent different kinds of values.
# Common types include integers, floats, strings, booleans, and NoneType.
# ================================================================================

# ---------------------------------------
# Examples of Different Data Types
# ---------------------------------------
a = 10        # int
b = 3.15      # float
c = "Hello"   # str (double quotes)
d = 'Hi'      # str (single quotes)
e = "1234"    # str (looks like a number, but it's a string)
f = True      # bool
g = False     # bool
h = None      # NoneType
i = ""        # str - empty string
j = " "       # str - contains a single space

# ---------------------------------------
# Using type() to Check Data Types
# ---------------------------------------
text   = "hi"
number = 10

print(type(text))    # ➜ <class 'str'>
print(type(number))  # ➜ <class 'int'>

# ---------------------------------------
# Exploring Methods for Each Data Type
# ---------------------------------------
# Some methods are specific to certain types.
print(text.upper())           # "HI" (string method)
print(number.bit_length())    # 4   (integer method)
# print(text.bit_length())    # Error: str has no bit_length()

# ---------------------------------------
# Python Challenge
# ---------------------------------------
# Create 5 variables, each with a different data type:
# - Your age
# - Your height (with decimals)
# - Your name
# - Are you a student?
# - Something with no value yet

age        = 30            # int
height     = 1.75          # float
name       = "Maria"       # str
is_student = False         # bool
has_kids   = None          # NoneType
