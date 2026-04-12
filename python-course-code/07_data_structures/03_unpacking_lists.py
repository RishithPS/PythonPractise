# ================================================================================
# LIST UNPACKING
# ----------------------------------------
# List unpacking allows us to assign list elements
# to multiple variables in a single line.
#
# The * (asterisk) collects remaining values.
# The _ (underscore) is commonly used to ignore values.
# ================================================================================


# ---------------------------------------
# Basic Unpacking with *
# ---------------------------------------
# * collects remaining middle values.

person = ['Maria', 29, 'Data Engineer', 'city', 'Spain']

name, *details, country = person

print(name)      # -> Maria  (first element)
print(details)   # -> [29, 'Data Engineer', 'city']  (middle values)
print(country)   # -> Spain  (last element)


# Star at the Beginning 
# * can also collect values from the start.

person = ['Maria', 29, 'Data Engineer', 'city', 'Spain']

*details, city, country = person

print(details)   # -> ['Maria', 29, 'Data Engineer']  (first values)
print(city)      # -> city
print(country)   # -> Spain


# Strings are iterable.
# * collects remaining characters.

numbers = 'Hi'

first, *rest = numbers

print(first)   # -> H
print(rest)    # -> ['i']


# the * variable becomes an empty list, if nothing to be collected

numbers = 'H'

first, *rest = numbers

print(first)   # -> H  (only character)
print(rest)    # -> []  (no remaining characters)


# ---------------------------------------
# Ignoring Values with _
# ---------------------------------------
# _ is used when we want to skip values.

person = ['Maria', 29, 'Data Engineer', 'Spain']

name, _, role, _ = person

print(name)   # -> Maria
print(role)   # -> Data Engineer


# ---------------------------------------
# Ignoring Multiple Values
# ---------------------------------------
# *_ ignores everything except the last element.

person = ['Maria', 29, 'Data Engineer', 'Spain']

*_, country = person

print(country)   # -> Spain
