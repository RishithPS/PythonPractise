# ================================================================================
# COPYING LISTS (REFERENCE • SHALLOW • DEEP)
# ----------------------------------------
# In Python, assigning a list to another variable
# does NOT create a new list.
#
# We must understand the difference between:
# - Assignment (reference)
# - Shallow copy
# - Deep copy
# ================================================================================


# ---------------------------------------
# Assignment (Reference Copy)
# ---------------------------------------
# Both variables point to the same object.

letters = ['a', 'b', 'c']

letters_copy = letters
letters_copy.append('z')

print('Original:', letters)      # -> ['a', 'b', 'c', 'z']
print('Copy:', letters_copy)     # -> ['a', 'b', 'c', 'z']
# Both changed (same memory reference)


# ---------------------------------------
# Shallow Copy with copy()
# ---------------------------------------
# Creates a new outer list.

letters = ['a', 'b', 'c']

letters_copy = letters.copy()
letters_copy.append('z')

print('Original:', letters)      # -> ['a', 'b', 'c']
print('Copy:', letters_copy)     # -> ['a', 'b', 'c', 'z']
# Only copy changed


# ---------------------------------------
# Shallow Copy with Nested Lists
# ---------------------------------------
# Inner lists are still shared.

matrix = [
    ['a', 'b'],   # Row 0
    ['c', 'd']    # Row 1
]

matrix_copy = matrix.copy()

matrix.pop()                     # remove last row
matrix_copy[0].append('z')       # modify inner list

print('Original:', matrix)       
print('Copy:', matrix_copy)
# Inner list modified in both (shared reference)


# ---------------------------------------
# Deep Copy
# ---------------------------------------
# Deep copy duplicates everything,
# including inner lists.

import copy

matrix = [
    ['a', 'b'],  # Row 0
    ['c', 'd'],  # Row 1
]

matrix_copy = copy.deepcopy(matrix)

matrix.pop()
matrix_copy[0].append('z')

print('Original:', matrix) 
print('Copy:', matrix_copy)      

# Completely independent


# ---------------------------------------
# Identity Comparison
# ---------------------------------------
# Using "is" to check memory identity.

import copy

original = [
    ['a', 'b'],  # Row 0
    ['c', 'd'],  # Row 1
]

# Assignment
copy1 = original
print("Same Object?", original is copy1)        # -> True

# Shallow Copy
copy2 = original.copy()
print("Same Object?", original is copy2)        # -> False
print("Shared Lists?", original[0] is copy2[0]) # -> True

# Deep Copy
copy3 = copy.deepcopy(original)
print("Same Object?", original is copy3)        # -> False
print("Shared Lists?", original[0] is copy3[0]) # -> False