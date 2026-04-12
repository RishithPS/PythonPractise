#===================================================================
# PRINT()
# ---------------------------------------
# The `print()` built-in Python function is used to display text
# on the screen. It’s your main way to *communicate* with users
# and check what your code is doing.
# You’ll use it in almost every Python program!
#===================================================================

print("Hi Python") # Double quotes
print('Hello Python') # Single quotes
# print("Hi') 

# Print a Header with Separators
print("--------------------")
print("    LEARN PYTHON    ")
print("--------------------")

# For Fun!
print("           __")
print("          / _)")
print("   .-^^^-/ /  ")
print("__/       /   ")
print("<__.|_|-|_|   ")

# ---------------------------------------
# ESCAPE SEQUENCES
# ---------------------------------------

# \" and \' - Print quotes inside strings

# print("Hi "Python"") #Invalid: Double quotes inside Double quotes
print("Hi \"Python\"") # Fix1: Use escape character (backslash)
print('Hi "Python"') # Fix2: Mix single and double quotes
# print('Hi 'Python'') #Invalid: Single quote inside Single quotes
print('Hi \'Python\'') # Fix1: Use escape character (backslash)
print("Hi 'Python'") # Fix2: Mix single and double quotes

# \\ - Backslash
print("Path: C:\Users\Baraa") #Invalid
print("Path: C:\\Users\\Baraa") 

# \n - New Line
print("Message1")
print()  # Blank Line
print("Message2")

print("Message1\n") # Adds one new line
print("Message2")

print("Message1\n\n\nMessage2")  # Adds three new lines
print("Message1\nMessage2") # One new line between

# \t - Tab
print("Message1\tMessage2")

# ---------------------------------------
# Python Challenge
# ---------------------------------------
# Recreate the following using ONLY ONE print() function:
# Your learning Path:
# 	 -Python Basics
# 	 -Data Engineering
# 	 -AI
# -----------------------------------------------

# Multi-line string with tabs
print("Your learning Path:\n\t-Python Basics\n\t-Data Engineering\n\t-AI")

# Alternative multi-line string using triple quotes
print("""Your learning Path:
\t- Python Basics
\t- Data Engineering
\t- AI""")

# ---------------------------------------
# PRINT() | Real Use Case for PRINT()
# ---------------------------------------

price_shirt = 25.00
price_jeans = 45.50

qty_shirt = 2
qty_jeans = 1

total_shirt = price_shirt * qty_shirt
total_jeans = price_jeans * qty_jeans
subtotal = total_shirt + total_jeans
print("Subtotal:", subtotal)
discount = subtotal * 0.10
print("Discount:", discount)
final_total = subtotal - discount
print("Final Total:", final_total)
