# ================================================================================
# WHITESPACE CLEANUP & CASE NORMALIZATION
# ----------------------------------------
# In real-world data, text is often messy.
# We need to:
# - Remove extra spaces
# - Normalize case (lower / upper)
#
# These operations are essential in data cleaning.
# ================================================================================


# ---------------------------------------
# Whitespace Cleanup
# ---------------------------------------
# lstrip()  → remove spaces from the left
# rstrip()  → remove spaces from the right
# strip()   → remove spaces from both sides

text = " Engineering".lstrip()
print(text) # -> Engineering

text = "Engineering ".rstrip()
print(text) # -> Engineering

text = "  Engineering ".strip()
print(text) # -> Engineering

text = "Data Engineering".strip()
print(text) # -> Data Engineering

# strip() can also remove specific characters.
text = "###Abc###".strip("#")
print(text) # -> Abc

# ---------------------------------------
# Case Conversion
# ---------------------------------------
# lower() → convert to lowercase
# upper() → convert to uppercase

text = "python PROGRAMMING"

print(text.lower()) # -> python programming
print(text.upper()) # -> PYTHON PROGRAMMING

# ---------------------------------------
# Why Normalization Matters
# ---------------------------------------
# When comparing user input, always normalize first.

search = "Email ".lower().strip()
data = " emAil".lower().strip()

print(search == data) # -> True
