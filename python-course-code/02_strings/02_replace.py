# ================================================================================
# STRING REPLACEMENT & CLEANUP
# ----------------------------------------
# In real projects, we often need to:
# - Replace characters
# - Normalize formats
# - Clean messy user input
#
# The replace() method is one of the most useful tools for this.
# ================================================================================


# ---------------------------------------
# Replacing Characters
# ---------------------------------------
# replace(old, new) replaces all occurrences.

price = "1234,56"

print(price.replace(",", ".")) # -> 1234.56


phone = "176-1234-56"

print(phone.replace("-", "/")) # -> 176/1234/56
print(phone.replace("-", "")) # -> 176123456


# ---------------------------------------
# Phone Number Cleanup Challenge
# ---------------------------------------
# Task:
# Convert messy phone number into clean digit-only format.
#
# Input:
# "+49 (176) 123-4567"
#
# Output:
# "00491761234567"

raw_number = "+49 (176) 123-4567"

clean_number = (
    raw_number
    .replace("+49", "0049")
    .replace("(", "")
    .replace(")", "")
    .replace("-", "")
    .replace(" ", "")
)

print(clean_number) # -> 00491761234567