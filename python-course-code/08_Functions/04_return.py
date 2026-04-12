# ================================================================================
# RETURN STATEMENT
# ----------------------------------------
# The return statement sends a value back
# from a function.
#
# Unlike print(), return allows us to:
# - Store the result in a variable
# - Reuse it later
# - Pass it to other functions
# ================================================================================


# ---------------------------------------
# Multiple Returns
# ---------------------------------------
# If the input is empty, we return None.
# Otherwise, we clean the name and return it.

def clean_name(name):
    if not name:
        return None
    else:
        cleaned = name.strip().lower()
        return cleaned

cln_name = clean_name(" MariA ")
print(cln_name)


# ---------------------------------------
# Returning Multiple Values
# ---------------------------------------
# A function can return more than one value.
# Python automatically packs them into a tuple.

def clean_name(name):
    lo_cleaned = name.strip().lower()
    up_cleaned = name.strip().upper()
    return lo_cleaned, up_cleaned

lo_name, up_name = clean_name(" MariA ")

print(lo_name)
print(up_name)
