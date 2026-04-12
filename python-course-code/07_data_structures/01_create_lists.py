# ================================================================================
# CREATING LISTS
# ----------------------------------------
# Lists are ordered, mutable collections in Python.
# They can store multiple values inside square brackets [].
# Lists can contain any data type, even mixed types.
# ================================================================================


# ---------------------------------------
# Empty Lists
# ---------------------------------------
# There are two common ways to create an empty list.

empty1 = []
print(empty1)

empty2 = list()
print(empty2)

# ---------------------------------------
# Creating a List from a String
# ---------------------------------------
# The list() function splits the string into individual characters.

letters = list('Python')
print(letters)


# ---------------------------------------
# Creating a List from range()
# ---------------------------------------
# range() generates numbers. list() converts them into a list.

numbers = list(range(5))
print(numbers)


# ---------------------------------------
# Nested List (Matrix)
# ---------------------------------------
# A list can contain other lists. This is commonly called a matrix.

matrix = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f']
]

print(matrix)
print(type(matrix))


# ---------------------------------------
# Mixed Data Types
# ---------------------------------------

mixed_matrix = [
    ['a', 'b'],
    [1, 2, 3],
    [True]
]

print(mixed_matrix)