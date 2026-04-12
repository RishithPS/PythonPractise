# ================================================================================
# TYPE CHECKING & NUMERIC VALIDATION
# ----------------------------------------
# Sometimes we need to verify:
# - Is this value an integer?
# - Is it a float?
# - What type is it?
#
# Python provides built-in tools for safe type checking.
# ================================================================================


# ---------------------------------------
# Checking if a Float Represents an Integer
# ---------------------------------------
# float.is_integer() checks whether
# a float has no decimal part.

x = 7.0
print(x.is_integer()) # -> True   (7.0 is float, but mathematically a whole number)

y = 7.1
print(y.is_integer()) # -> False  (7.1 has decimal part)


# ---------------------------------------
# Type Checking with isinstance()
# ---------------------------------------
# isinstance() checks if a value
# belongs to a specific type.

x = 70.4
print(isinstance(x, int)) # -> False
print(isinstance(x, float)) # -> True

# ---------------------------------------
# Checking Multiple Types
# ---------------------------------------
# You can check against multiple types at once.

value = 10
print(isinstance(value, (int, float))) # -> True  (value is numeric)

# ---------------------------------------
# type() vs isinstance()
# ---------------------------------------
# type() returns the exact type.
# isinstance() is preferred in real projects.

print(type(value)) # -> <class 'int'>

