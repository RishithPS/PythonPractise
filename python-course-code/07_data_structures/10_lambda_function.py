# ================================================================================
# LAMBDA FUNCTIONS
# ----------------------------------------
# A lambda function is a small anonymous function.
# It is useful when we need a quick function
# without formally defining it using def.
# ================================================================================


# ---------------------------------------
# Basic Lambda Examples
# ---------------------------------------

# Multiply a number by 2
# We create a short function in one line.

multiple = lambda x: x * 2
print(multiple(2))

# Add two numbers
add = lambda x, y: x + y
print(add(1, 2))

# Check membership in a string
check = lambda i: i in "python"
print(check('z'))

# Convert price string to float
prices = ['$12.50', '$9.99', '$100.00']
print(list(map(lambda p: float(p.replace('$', '')), prices)))

# ---------------------------------------
# Lambda with filter() & sorted ()
# ---------------------------------------

# Example 6: Keep only prices >= 100
prices = [120, 30, 300, 80]
print(list(filter(lambda p: p >= 100, prices)))

students = [
    ['Maria', 85],
    ['Kumar', 90],
    ['Max', 60]
]
# Keep students with score > 70
print(list(filter(lambda row: row[1] > 70, students)))

# Keep only students with names starting with 'M'
print(list(filter(lambda row: row[0].startswith('M'), students)))

# Sort students by their scores (ascending)
print(sorted(students, key=lambda row: row[1]))
