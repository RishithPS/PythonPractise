# ================================================================================
# MODIFYING LISTS (ADD • REMOVE • UPDATE)
# ----------------------------------------
# Lists are mutable.
# This means we can add, remove, and update elements.
# Python provides several built-in methods to do that.
# ================================================================================

# ================================================================================
# Adding Items to Lists
# ================================================================================

# ---------------------------------------
# append()
# ---------------------------------------
# Adds element to the end of the list.

letters = ['a', 'b', 'c']

letters.append('x')
letters.append('y')
print(letters)   # -> ['a', 'b', 'c', 'x', 'y']  (added at end)


# ---------------------------------------
# insert()
# ---------------------------------------
# Adds element at a specific index.

letters = ['a', 'b', 'c']

letters.insert(0, 'x')
letters.insert(3, 'y')
print(letters)   # -> ['x', 'a', 'b', 'y', 'c']


# ---------------------------------------
# Adding to Matrix
# ---------------------------------------
# Adding Rows to a Matrix

matrix = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    ['g', 'h', 'i']
]

matrix.append(['x', 'y', 'z'])
matrix.insert(0, ['a', 'a', 'a'])
print(matrix)


# Adding One Item to Matrix

matrix = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    ['g', 'h', 'i']
]

matrix[1].append('x')
matrix[0].insert(0, 'z')
print(matrix)


# ================================================================================
# Removing Items From Lists
# ================================================================================

# ---------------------------------------
# clear()
# ---------------------------------------
# Removes all elements.

letters = ['a', 'b', 'c']

letters.clear()
print(letters)   # -> []  (list is now empty)


# ---------------------------------------
# remove()
# ---------------------------------------
# Removes first occurrence of value.

letters = ['a', 'b', 'a']

letters.remove('a')
letters.remove('a')
print(letters)   # -> ['b']


# ---------------------------------------
# pop()
# ---------------------------------------
# Removes element by index and returns it.

letters = ['a', 'b', 'c']
removed = letters.pop(1)
print(letters)           # -> ['a', 'c']
print('Removed Item:', removed)   # -> b


# ---------------------------------------
# Removing Inside Nested Lists
# ---------------------------------------

matrix = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    ['g', 'h', 'i']
]

matrix[1].remove('e')   # remove specific value
matrix[-1].pop(0)       # remove by index
matrix[0].pop()         # remove last element
print(matrix)


# ================================================================================
# Updating Items in Lists
# ================================================================================

# Direct assignment changes values.

letters = ['a', 'b', 'c']

letters[0] = 'x'
letters[1] = 'y'
letters = 'z'   # variable now points to a string
print(letters)        # -> z
print(type(letters))  # -> <class 'str'>



# Updating Nested Lists

matrix = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    ['g', 'h', 'i']
]

matrix[-1] = ['x', 'y', 'z']   # replace entire row
matrix[0][0] = '-'             # update specific element
matrix[1][1] = '-'
matrix[-1][-1] = '-'
print(matrix)