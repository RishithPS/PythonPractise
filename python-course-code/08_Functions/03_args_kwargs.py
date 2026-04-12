# ================================================================================
# VARIABLE ARGUMENTS (*args • **kwargs)
# ----------------------------------------
# Sometimes we don’t know how many inputs
# a function will receive.
#
# Python allows flexible arguments using:
# - *args  → multiple positional arguments
# - **kwargs → multiple keyword arguments
# ================================================================================


# ---------------------------------------
# *args (Multiple Positional Arguments)
# ---------------------------------------
# Here we want to calculate the total of an unknown number of values.
def total(*args):
    print(type(args))     # args is a tuple
    print(sum(args))

total(1, 2)
total(1, 2, 3)
total(1, 2, 3, 4)

# ---------------------------------------
# **kwargs (Multiple Keyword Arguments)
# ---------------------------------------
# Here we want to build a flexible user profile.
# We don’t know which fields the user will provide.

def create_user(**kwargs):
    print(type(kwargs))   # kwargs is a dictionary
    print(kwargs)

create_user(
    first_name="Mo",
    last_name="Salah",
    age=33,
    country="Egypt"
)
create_user(
    name="Ronaldo",
    country="Portugal"
)