# ================================================================================
# ACCESSING & READING LISTS
# ----------------------------------------
# Lists are ordered collections.
# Each element has an index position.
# We use indexing and slicing to access values.
# ================================================================================


# ---------------------------------------
# Basic Indexing
# ---------------------------------------
# Accessing elements using position.

lst = ['a', 'b', 'c', 'd']

print(lst)                     # -> ['a', 'b', 'c', 'd']  (entire list)
print(lst[0])                  # -> a  (first element)
print(lst[-1])                 # -> d  (last element)
print(lst[len(lst) - 1])       # -> d  (last using length)


# ---------------------------------------
# Nested List Indexing (Matrix)
# ---------------------------------------
# Accessing elements inside a list of lists.

matrix = [
    ['a', 'b', 'c'],  # Row 0
    ['d', 'e', 'f'],  # Row 1
    ['g', 'h', 'i']   # Row 2
]

print(matrix[-1])        # -> ['g', 'h', 'i']  (last row)
print(matrix[-1][-1])    # -> i  (last element in row)
print(matrix[0][0])      # -> a  (row 0, column 0)
print(matrix[1][1])      # -> e  (middle element)


# ---------------------------------------
# Slicing
# ---------------------------------------
# Format: list[start:stop]
# Stop index is excluded.

lst = ['a', 'b', 'c', 'd']

print(lst)       # -> ['a', 'b', 'c', 'd']  (full list)
print(lst[0])    # -> a  (first element)
print(lst[-1])   # -> d  (last element)
print(lst[-2])   # -> c  (second last)
print(lst[:2])   # -> ['a', 'b']  (first two)
print(lst[2:])   # -> ['c', 'd']  (from index 2)
print(lst[:])    # -> ['a', 'b', 'c', 'd']  (copy of list)


# ---------------------------------------
# Slicing Inside Nested Lists
# ---------------------------------------
# Combine indexing + slicing.

matrix = [
    ['a', 'b', 'c'],  # Row 0
    ['d', 'e', 'f'],  # Row 1
    ['g', 'h', 'i']   # Row 2
]

print(matrix[2][:2])   # -> ['g', 'h']  (first two of last row)