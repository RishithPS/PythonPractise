# ================================================================================
# SORTING & REVERSING LISTS
# ----------------------------------------
# Python provides multiple ways to sort and reverse lists.
# Some methods modify the original list.
# Others return a new list without changing the original.
# ================================================================================

# ---------------------------------------
# sort() – Ascending
# ---------------------------------------
# sort() modifies the original list.

letters = ['c', 'a', 'b']
letters.sort()
print(letters)   # -> ['a', 'b', 'c']  (sorted ascending)


# ---------------------------------------
# sort() – Descending
# ---------------------------------------
# reverse=True sorts in descending order.

letters = ['c', 'a', 'b']
letters.sort(reverse=True)
print(letters)   # -> ['c', 'b', 'a']  (sorted descending)


# ---------------------------------------
# Sorting Nested Lists
# ---------------------------------------
# Lists are compared element by element.

matrix = [
    ['d', 'e', 'f'],
    ['a', 'z', 'i'],
    ['a', 'a', 'c']
]

matrix.sort()
print(matrix)


# ---------------------------------------
# Sorting Only One Row
# ---------------------------------------
# We can sort individual rows.

matrix = [
    ['d', 'e', 'f'],
    ['a', 'z', 'i'],
    ['a', 'a', 'c']
]

matrix[1].sort()
print(matrix)


# ---------------------------------------
# sorted() – Returns New List
# ---------------------------------------
# Does NOT modify the original list.

letters = ['c', 'a', 'b']

new_list = sorted(letters, reverse=True)
print('Original List:', letters)   # -> ['c', 'a', 'b']
print('Sorted List:', new_list)    # -> ['c', 'b', 'a']


# ---------------------------------------
# reversed() – Reverse Order
# ---------------------------------------
# reversed() returns an iterator.
# We convert it to list.

letters = ['c', 'a', 'b']

new_list = list(reversed(letters))
print('Original List:', letters)    # -> ['c', 'a', 'b']
print('Reversed List:', new_list)   # -> ['b', 'a', 'c']