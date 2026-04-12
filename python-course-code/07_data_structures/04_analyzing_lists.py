# ================================================================================
# EXPLORING & ANALYZING LISTS
# ----------------------------------------
# Python provides many built-in functions to analyze lists.
# These help us inspect values, check conditions,
# and compare lists efficiently.
# ================================================================================


# ---------------------------------------
# Basic Analysis Functions
# ---------------------------------------

numbers = [1, 5, 5, 4, 3]

print("Max:", max(numbers))        # -> 5  (largest value)
print("Min:", min(numbers))        # -> 1  (smallest value)
print("Sum:", sum(numbers))        # -> 18 (total of elements)
print("Length:", len(numbers))     # -> 5  (number of elements)


# ---------------------------------------
# all()
# ---------------------------------------
# Returns True if all elements are truthy.

print("All:", all(numbers))            # -> True  (no zero values)
print("All:", all([1, 0, 2]))          # -> False (0 is falsy)
print("All:", all(['a', '', 'b']))     # -> False (empty string is falsy)
print("All:", all(['a', 'c', 'b']))    # -> True  (all non-empty)

# ---------------------------------------
# any()
# ---------------------------------------
# Returns True if at least one element is truthy.

print("Any:", any(numbers))            # -> True  (non-zero values exist)
print("Any:", any([1, 0, 2]))          # -> True  (1 and 2 are truthy)
print("Any:", any(['a', '', 'b']))     # -> True  (non-empty string exists)
print("Any:", any([0, 0, 0]))          # -> False (all values are falsy)

# ---------------------------------------
# count() and index()
# ---------------------------------------

print("Count:", numbers.count(5))   # -> 2  (5 appears twice)
print("Index:", numbers.index(5))   # -> 1  (first occurrence position)

# ---------------------------------------
# Membership Operators
# ---------------------------------------

print(8 in numbers)        # -> False
print(8 not in numbers)    # -> True

# ---------------------------------------
# Equality Comparison
# ---------------------------------------
# == compares values.

list1 = [1, 2, 3, 4]
list2 = [1, 2, 3]

print(list1 == list2)      # -> False (different length)

# ---------------------------------------
# Lexicographical Comparison
# ---------------------------------------
# Lists are compared element by element.

list1 = [1, 2, 3]
list2 = [5, 2, 3]

print(list1 < list2)       # -> True (1 < 5)


# ---------------------------------------
# Identity Comparison
# ---------------------------------------
# is checks memory identity, not value.

list1 = [5, 8, 3]
list2 = [5, 8, 3]

print(list1 is list2)      # -> False (different objects in memory)
# ================================================================================