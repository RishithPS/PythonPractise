# ================================================================================
# FUNCTIONS (WHY • BUILT-IN • USER-DEFINED)
# ----------------------------------------
# Functions help us avoid repetition.
# Instead of writing the same code again and again,
# we define it once and reuse it.
# ================================================================================


# ---------------------------------------
# Problem: Repetition
# ---------------------------------------
# Here we repeat the same coffee steps multiple times.

print("Wake up")
print("Start Machine")
print("Make Coffee")
print("Add Milk")
print("Enjoy it")

print("Working for a while")

print("Start Machine")
print("Make Coffee")
print("Add Milk")
print("Enjoy it")


# ---------------------------------------
# Solution: Create a Function
# ---------------------------------------
# We define the steps once, then call them whenever we need.

def make_coffee():
    print("Start Machine")
    print("Make Coffee")
    print("Add Milk")
    print("Enjoy it")


print("Wake up")
make_coffee()
print("Working for a while")
make_coffee()
make_coffee()


# ---------------------------------------
# Python Function Sources
# ---------------------------------------

import math


# Example 1: Built-in Function
# Already available in Python.
print(len("Python"))   # -> 6


# Example 2: Function from a Library
# We import first, then call it.
number = 4.2
print(math.ceil(number))   # -> 5


# Example 3: User-Defined Function
# We define it ourselves using def.

def greet():
    print("Hello")

greet()   # -> Hello
