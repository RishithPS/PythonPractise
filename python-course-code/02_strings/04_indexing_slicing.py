# ================================================================================
# STRING INDEXING & SLICING
# ----------------------------------------
# Strings are ordered sequences of characters.
# This means:
# - Each character has a position (index)
# - Indexing starts at 0
# - Negative indexing starts from the end
# ================================================================================

# ---------------------------------------
# Basic Indexing
# ---------------------------------------
# Access characters by position.

text = "Python"

print(text[0]) # -> P  (first character)
print(text[-6]) # -> P  (same as index 0)
print(text[5]) # -> n  (last character)
print(text[-1]) # -> n  (last character using negative index)
print(text[3]) # -> h

# ---------------------------------------
# Slicing
# ---------------------------------------
# Format: string[start:stop]
# Stop index is excluded.

date = "2026-09-20"

print(date[0:4]) # -> 2026  (year)
print(date[:4]) # -> 2026  (from start to index 4)
print(date[5:7]) # -> 09  (month)
print(date[8:]) # -> 20  (from index 8 to end)
print(date[-2:]) # -> 20  (last two characters)