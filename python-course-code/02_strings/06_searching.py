# ================================================================================
# STRING SEARCH & PARTIAL EXTRACTION
# ----------------------------------------
# In real-world applications, we often need to:
# - Check if text starts or ends with something
# - Search for substrings
# - Extract parts of a string dynamically
# ================================================================================

# ---------------------------------------
# Search Functions
# ---------------------------------------
# startswith() → checks beginning of string
# endswith()   → checks ending of string
# "in"         → checks if substring exists

phone = "+48-176-12345"
print(phone.startswith("+49")) # -> False


email = "baraa@outlook.com"
print(email.endswith("gmail.com")) # -> False


file = "data_backup.csv"
print(file.endswith(".csv")) # -> True
print("@" in email) # -> True


url = "https://api.company.com/v1/data"
print("/api" in url) # -> True

# ---------------------------------------
# Partial Extraction Using find()
# ---------------------------------------
# find() returns the position of the first match.
# If not found → returns -1.

phone1 = "+48-176-12345"
phone2 = "48-654-16548"
phone3 = "0048-654-16548"
print(phone1.find("-")) # -> 3  (index of first "-")

# Extract everything after first "-"
print(phone1[phone1.find("-") + 1:]) # -> 176-12345
print(phone2[phone2.find("-") + 1:]) # -> 654-16548
print(phone3[phone3.find("-") + 1:]) # -> 654-16548

