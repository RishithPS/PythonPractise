# ================================================================================
# FOR LOOPS
# ----------------------------------------
# A for loop allows you to repeat code automatically.
# Instead of writing the same print statement many times,
# Python iterates over a collection and executes the block
# for each item inside it.
# ================================================================================


# ---------------------------------------
# Without Loop
# ---------------------------------------
# Here we manually print multiple rounds.
# This works, but it does not scale well.

print("Round: 2")
print("Round: 3")
print("Round: 4")
print("Round: 5")


# ---------------------------------------
# Looping Over a Tuple
# ---------------------------------------
# Instead of repeating code, we store values inside a tuple and iterate over them.

items = (1, 2, 3, 4, 5)

for item in items:
    print(f"Round: {item}")


# ---------------------------------------
# Looping Over a String
# ---------------------------------------
# A string is iterable. Python goes character by character.

items = "Python"

for item in items:
    print(f"Round: {item}")


# ---------------------------------------
# Using range()
# ---------------------------------------
# range(start, stop, step)
# The stop value is excluded.

for item in range(2, 10, 2):
    print(f"Round: {item}")


# ---------------------------------------
# Accumulator Pattern
# ---------------------------------------
# We initialize a variable outside the loop and update it during each iteration.
# Very common in analytics and data processing.

scores = [80, 50, 60, 75]
total = 0

for score in scores:
    total += score
    print("Current Total:", total)

print("Final Total:", total)


# ---------------------------------------
# Cleaning Data Inside a Loop
# ---------------------------------------
# Cleaning file names before processing them.

files = [' Report.csv ', 'DATA.csv ', ' final.TXT']

for file in files:
    file = file.strip().lower().replace('.txt', '.csv')
    print(f"Processing {file}")


# ---------------------------------------
# Python Challenge
# ---------------------------------------
# Print the 7-times table from 1 to 10
#
# 7 x 1  = 7
# 7 x 2  = 14
# 7 x 3  = 21
# 7 x 4  = 28
# 7 x 5  = 35
# 7 x 6  = 42
# 7 x 7  = 49
# 7 x 8  = 56
# 7 x 9  = 63
# 7 x 10 = 70

for i in range(1, 11):
    print(f"7 x {i} = {7*i}")


# ---------------------------------------
# Python Challenge
# ---------------------------------------
# Print a left-aligned pyramid of stars
# with 6 rows using a for loop.
#
# *
# **
# ***
# ****
# *****
# ******

for i in range(1, 7):
    print("*" * i)