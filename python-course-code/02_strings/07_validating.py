# ================================================================================
# STRING VALIDATION METHODS
# ----------------------------------------
# Python provides built-in string methods
# to validate the content of text.
#
# These are extremely useful in:
# - User input validation
# - Form processing
# - Data cleaning
# - ETL pipelines
# ================================================================================

# ---------------------------------------
# isalpha()
# ---------------------------------------
# Returns True if ALL characters are letters.
# No spaces, no numbers, no symbols allowed.

name = "Michael"
print(name.isalpha()) # -> True

name = "Michael123"
print(name.isalpha()) # -> False

name = "Michael Scott"
print(name.isalpha()) # -> False  (space is not a letter)


# ---------------------------------------
# isnumeric()
# ---------------------------------------
# Returns True if ALL characters are numeric.
# Includes special numeric characters.

age = "25"
print(age.isnumeric()) # -> True

age = "25.5"
print(age.isnumeric()) # -> False  (decimal point is not numeric)

age = "25a"
print(age.isnumeric()) # -> False

# ---------------------------------------
# isdigit()
# ---------------------------------------
# Similar to isnumeric() but slightly stricter.
# Used mostly for digit-only strings.

code = "12345"
print(code.isdigit()) # -> True

code = "123a"
print(code.isdigit()) # -> False

# ---------------------------------------
# isalnum()
# ---------------------------------------
# Returns True if string contains
# only letters and numbers (no spaces).

username = "User123"
print(username.isalnum()) # -> True

username = "User 123"
print(username.isalnum()) # -> False