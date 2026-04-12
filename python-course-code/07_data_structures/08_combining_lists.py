# ================================================================================
# COMBINING LISTS
# ----------------------------------------
# There are multiple ways to combine lists in Python.
# Some create a new list.
# Others modify the existing list.
#
# We can also combine elements pairwise using zip().
# ================================================================================


# ---------------------------------------
# + Operator
# ---------------------------------------
# Creates a new combined list.

letters = ['a', 'b', 'c']
numbers = [1, 2, 3]

print(letters + numbers)   # -> ['a', 'b', 'c', 1, 2, 3]


# ---------------------------------------
# extend()
# ---------------------------------------
# Modifies the original list.

letters = ['a', 'b', 'c']
numbers = [1, 2, 3]

numbers.extend(letters)

print(letters)   # -> ['a', 'b', 'c']  (unchanged)
print(numbers)   # -> [1, 2, 3, 'a', 'b', 'c']


# ---------------------------------------
# zip()
# ---------------------------------------
# Combines elements position by position.
# Stops at shortest iterable.

letters = ['a', 'b', 'c']
numbers = [1, 2, 3, 4]

comb = list(zip(letters, numbers, "Hi"))

print(comb) # -> [('a', 1, 'H'), ('b', 2, 'i')]



# Practical Example (IDs + Names)

ids = [101, 102, 103]
names = ['Ali', 'Sara', 'John']

print(list(zip(ids, names))) # -> [(101, 'Ali'), (102, 'Sara'), (103, 'John')]

