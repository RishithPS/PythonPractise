# ================================================================================
# NUMERIC DATA TYPES & BASIC NUMBER TOOLS
# ----------------------------------------
# Python supports different numeric types:
# - int      → Whole numbers
# - float    → Decimal numbers
# - complex  → Numbers with imaginary part
#
# We can convert between types and perform arithmetic operations.
# ================================================================================


# ---------------------------------------
# Numeric Types
# ---------------------------------------

x = 5
y = 5.7
z = 2 + 3j

print(type(x))  # -> <class 'int'>
print(type(y))  # -> <class 'float'>
print(type(z))  # -> <class 'complex'>


# ---------------------------------------
# Type Conversion
# ---------------------------------------
# Convert values between numeric types.

x = "24"
print(type(x))  # -> <class 'str'>

x = int(x)      # Convert string to integer
print(type(x))  # -> <class 'int'>
print(x * 3)    # -> 72

x = 3.14
print(int(x))   # -> 3 (decimal part removed)

x = 3
print(float(x)) # -> 3.0

x = 3
y = 4
print(complex(x, y))  # -> (3+4j)


# ---------------------------------------
# Basic Arithmetic Operations
# ---------------------------------------

print(2 + 3)     # -> 5   (Addition)
print(5 - 3)     # -> 2   (Subtraction)
print(4 * 2)     # -> 8   (Multiplication)
print(7 / 2)     # -> 3.5 (True division → float)
print(7 // 2)    # -> 3   (Floor division → integer result)
print(9 % 2)     # -> 1   (Modulus → remainder)
print(2 ** 3)    # -> 8   (Exponentiation)


# ---------------------------------------
# Compound Assignment Operators
# ---------------------------------------
# Shorter way to update a variable.

x = 2

x += 3
print(x)  # -> 5

x -= 1
print(x)  # -> 4

x *= 2
print(x)  # -> 8

# ---------------------------------------
# Useful Built-in Numeric Functions
# ---------------------------------------

print(abs(-10))   # -> 10  (Absolute value)
print(pow(2, 3))  # -> 8   (Power function)
print(divmod(7, 2))  # -> (3, 1) (Quotient, Remainder)
