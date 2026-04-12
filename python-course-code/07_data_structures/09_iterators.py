# ================================================================================
# ITERATION TOOLS (ENUMERATE • REVERSED • ZIP • MAP • FILTER)
# ----------------------------------------
# Python gives us powerful tools to work with iterables.
# Instead of writing everything manually,
# we can transform, combine, and filter data more efficiently.
# ================================================================================


# ---------------------------------------
# Basic Iteration with Transformation
# ---------------------------------------

# Convert letters to uppercase manually
letters = ['a', 'b', 'c']
new_list = []

for l in letters:
    new_list.append(l.upper())
    print(new_list)

# ---------------------------------------
# enumerate()
# ---------------------------------------

# Get index and value together
letters = ['a', '', 'c']

for index, value in enumerate(letters):
    print(index, value)

# ---------------------------------------
# reversed()
# ---------------------------------------

# Iterate from the end to the beginning
letters = ['a', 'b', 'c']

for l in reversed(letters):
    print(l)

# ---------------------------------------
# zip()
# ---------------------------------------

# Combine two related lists
letters = ['a', 'b', 'c']
numbers = [1, 2, 3]

for l, n in zip(letters, numbers):
    print(l, n)

# ---------------------------------------
# map()
# ---------------------------------------

# Convert letters to uppercase automatically
letters = ['a', 'b', 'c']
print(list(map(str.upper, letters)))

# Convert string numbers to integers
numbers = ['1', '2', '3']
print(list(map(int, numbers)))

# Clean extra spaces from names
names = [' Maria ', ' John ', ' Kumar']

for n in map(str.strip, names):
    print(n)

# ---------------------------------------
# filter()
# ---------------------------------------

# Remove falsy values
letters = ['a', '', 'b', None, 'c', False]
print(list(filter(bool, letters)))


# Task: Keep only alphabetic values
items = ['sql', '123', 'python', '42']

for i in filter(str.isalpha, items):
    print(i)
