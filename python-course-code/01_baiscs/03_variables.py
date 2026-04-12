# ================================================================================
# VARIABLES 
# ----------------------------------------
# Variables act as named containers for storing data in Python.
# You give a variable a value using the assignment operator `=`, then
# you can reuse that name throughout your code. We’ll also use
# the `print()` function to display both literals and variables.
# ================================================================================

# ---------------------------------------
# Without Variables
# ---------------------------------------
# Here we print fixed text directly using print().
print("My name is Baraa")
print("Baraa is learning Python")
print("Baraa wants to become Python expert")


# ---------------------------------------
# Single Variable
# ---------------------------------------
# Store your name in a variable and reuse it in print().
name = "Baraa"
print("My name is", name)
print(name, "is learning Python")
print(name, "wants to become Python expert")


# ---------------------------------------
# Multiple Variables
# ---------------------------------------
# Now we’ll keep both your name and the language in variables.
name     = "Baraa"
language = "python"
print("My name is", name)
print(name, "is learning", language)
print(name, "wants to become", language, "expert")

# ---------------------------------------
# Python Challenge
# ---------------------------------------
# Print the following three lines:
#     info@datawithbaraa.com
#     support@datawithbaraa.com
#     www.datawithbaraa.com
# Use a variable for the base domain to make it dynamic!

domain = "datawithbaraa.com"
print("info@" + domain)
print("support@" + domain)
print("www." + domain)
