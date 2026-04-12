# ================================================================================
# STRING COMBINING • FORMATTING • SPLITTING
# ----------------------------------------
# Strings are not just text.
# We often:
# - Combine them
# - Format them
# - Split them into structured data
# ================================================================================


# ---------------------------------------
# Combining Strings
# ---------------------------------------
# We can concatenate strings using +.

first_name = "Michael"
last_name = "Scott"

full_name = first_name + "-" + last_name
print(full_name) # -> Michael-Scott


folder = "C:/Users/Baraa/"
file = "report.csv"

full_file_path = folder + file
print(full_file_path) # -> C:/Users/Baraa/report.csv

# ---------------------------------------
# String Formatting
# ---------------------------------------
# Formatting allows us to insert variables into text.

name = "Sam"
age = 34
is_student = False

# Method 1: String Concatenation (Old Style)
print("My name is " + name + ", I am " + str(age) +
      " years old, and student status is " + str(is_student) + ".")

# Method 2: f-Strings (Recommended)
# Cleaner, more readable, and powerful.

print(f"My name is {name}, I am {age} years old, and student status is {is_student}.")

# f-String Expressions
# We can evaluate expressions inside {}.
print(f"2 + 3 = {2 + 3}") # -> 2 + 3 = 5

# Escaping Curly Braces
print(f"{{This is me}}") # -> {This is me}

# ---------------------------------------
# Splitting Strings
# ---------------------------------------
# split() separates a string into a list.

stamp = "2026-09-20 14:30"
print(stamp.split(" ")) # -> ['2026-09-20', '14:30']


csv_file = "1234,Max,USA,1970-10-05,M"
print(csv_file.split(",")) # -> ['1234', 'Max', 'USA', '1970-10-05', 'M']

