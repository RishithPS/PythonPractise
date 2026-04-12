# ================================================================================
# Data Structures Behavior
# ----------------------------------------
# Python provides multiple built-in collection types.
# Each one has different behavior regarding:
# - Order
# - Mutability
# - Duplicates
# - Indexing
# ================================================================================


# ---------------------------------------
# List
# ---------------------------------------
# Lists are: Ordered, Mutable, Allow duplicates, Indexed

my_list = [10, 30, 20, 10]

print(my_list)       # -> [10, 30, 20, 10]  (ordered, duplicates allowed)
print(my_list[1])    # -> 30  (indexed access)
my_list[3] = 40      # Modify element
print(my_list)       # -> [10, 30, 20, 40]


# ---------------------------------------
# Tuple
# ---------------------------------------
# Tuples are: Ordered, Immutable, Allow duplicates, Indexed

my_tuple = (10, 30, 20, 10)

print(my_tuple)         # -> (10, 30, 20, 10)
print(my_tuple[1])      # -> 30  (indexed access)
# my_tuple[3] = 40      # ❌ Error (immutable)
print(sorted(my_tuple)) # -> [10, 10, 20, 30]  (sorted returns a new list)



# ---------------------------------------
# Set
# ---------------------------------------
# Sets are: Unordered, Mutable, Unique values only, Not indexed

my_set = {10, 30, 20, 10}

print(my_set)       # -> {10, 20, 30}  (duplicates removed)
# print(my_set[1])  # ❌ Error (not indexed)
my_set.remove(20)
print(my_set)       # -> {10, 30}


# ---------------------------------------
# Dictionary
# ---------------------------------------
# Dictionaries are: Ordered (Python 3.7+), Mutable, Keys are unique, Accessed by key

my_dict = {
    'a': 10,
    'b': 20,
    'c': 20,
    'a': 40   # Duplicate key overrides previous
}

print(my_dict)       # -> {'a': 40, 'b': 20, 'c': 20}
print(my_dict['b'])  # -> 20  (key-based access)
my_dict['c'] = 80    # Update value
print(my_dict)       # -> {'a': 40, 'b': 20, 'c': 80}

