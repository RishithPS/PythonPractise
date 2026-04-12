# ================================================================================
# RANDOM MODULE (SIMULATION • SAMPLING • SHUFFLING)
# ----------------------------------------
# The random module allows us to generate
# unpredictable values.
#
# Used in:
# - Games
# - Simulations
# - Data Sampling
# - Testing
# - Machine Learning experiments
# ================================================================================


import random


# ---------------------------------------
# random()
# ---------------------------------------
# Returns a float between 0.0 and 1.0

print(random.random())

# ---------------------------------------
# randint()
# ---------------------------------------
# Returns an integer between two values (inclusive)

print(random.randint(1, 6))

# ---------------------------------------
# uniform()
# ---------------------------------------
# Returns a random float between two numbers

print(random.uniform(10, 20))
# -> Example: 14.8271


# ---------------------------------------
# choice()
# ---------------------------------------
# Select one random element from a sequence

colors = ["red", "blue", "green"]
print(random.choice(colors)) 

# ---------------------------------------
# shuffle()
# ---------------------------------------
# Shuffles a list in place (modifies original list)

numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)

print(numbers)

# ---------------------------------------
# sample()
# ---------------------------------------
# Select multiple unique random elements

students = ["Ali", "Sara", "John", "Maria", "Kumar"]

print(random.sample(students, 2))

# ---------------------------------------
# seed()
# ---------------------------------------
# Controls randomness for reproducibility.
# Same seed -> same results every run.

random.seed(42)
print(random.randint(1, 10))