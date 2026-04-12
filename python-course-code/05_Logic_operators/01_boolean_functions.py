# ================================================================================
# BOOLEAN VALUES
# ----------------------------------------
# Booleans are either True or False. They're often used for logic, conditions,
# validations, and control flow. Python also allows checking "truthiness" of values.
# ================================================================================

# ---------------------------------------
# Basic Boolean Values
# ---------------------------------------
print(True)         # ➜ True
print(False)        # ➜ False
print(type(True))   # ➜ <class 'bool'>

# ---------------------------------------
# bool() Function: Truthiness of Values
# ---------------------------------------
print(bool(123))     # ➜ True  (non-zero number)
print(bool("Hi"))    # ➜ True  (non-empty string)

print(bool(()))      # ➜ False (empty tuple)
print(bool(0))       # ➜ False (zero)
print(bool(""))      # ➜ False (empty string)
print(bool(None))    # ➜ False (None is always considered False)

# ---------------------------------------
# Using any() and all() for Field Validation
# ---------------------------------------
email    = ""
phone    = "017-1234"
username = "baraa123"

# Allows registration if at least one field is filled
print(any([email, phone, username]))  # ➜ True

# Allows registration only if all fields are filled
print(all([email, phone, username]))  # ➜ False

# ---------------------------------------
# Type Checking with isinstance()
# ---------------------------------------
print(isinstance(123, int))     # ➜ True
print(isinstance(True, str))    # ➜ False

# ---------------------------------------
# String Start/End Checks
# ---------------------------------------
print("Hello".endswith("o"))    # ➜ True
print("Hello".startswith("o"))  # ➜ False
