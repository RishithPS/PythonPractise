# ================================================================================
# SETS (UNIQUE • MATHEMATICAL OPERATIONS • RELATIONSHIPS)
# ----------------------------------------
# Sets are:
# - Unordered
# - Mutable
# - Unique values only
# - Not indexed
# ================================================================================


# ---------------------------------------
# Basic Set Behavior
# ---------------------------------------
my_set = {10, 30, 20, 10}
print(my_set)       # -> {10, 20, 30}  (duplicates removed)
# print(my_set[1])  # ❌ Error (not indexed)
my_set.remove(20)   # Remove specific value
print(my_set)       # -> {10, 30}


# ---------------------------------------
# Basic Set Operations
# ---------------------------------------
a = {10, 20, 30, 40}
a.add(50)       # Add one value
a |= {1, 2}     # Add multiple values (union assignment)
a.discard(100)  # Safe remove (no error if not found)
print(a)

# ---------------------------------------
# Mathematical Operations
# ---------------------------------------
# Sets support mathematical set theory operations.

a = {10, 20, 30, 40}
b = {30, 40, 50, 60}


# Union (combine all unique elements)
print(a.union(b))   # -> {10, 20, 30, 40, 50, 60}
print(a | b)        # Same as union

# Intersection (common elements)
print(a.intersection(b))   # -> {30, 40}
print(a & b)               # Same as intersection

# Difference (elements in a but not in b)
print(a.difference(b))   # -> {10, 20}
print(a - b)             # Same as above
print(b - a)             # -> {50, 60}

# Symmetric Difference (elements in either but not both)
print(a.symmetric_difference(b))   # -> {10, 20, 50, 60}
print(a ^ b)                       # Same as above


# ---------------------------------------
# Relationship Operations
# ---------------------------------------
# Check subset, superset, and disjoint relationships.

a = {10, 20}
b = {30, 40, 50, 60}

print(a.issubset(b))     # -> False  (a not fully inside b)
print(b.issuperset(a))   # -> False  (b does not contain 10, 20)

print(a.isdisjoint(b))   # -> True   (no common elements)
