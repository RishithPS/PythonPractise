# ================================================================================
# DICTIONARIES (KEY • VALUE • LOOKUPS • COMPREHENSION)
# ----------------------------------------
# Dictionaries are:
# - Ordered (Python 3.7+)
# - Mutable
# - Keys must be unique
# - Accessed using keys (not index)
# ================================================================================


# ---------------------------------------
# Basic Dictionary Behavior
# ---------------------------------------
# Dictionaries are: Ordered (Python 3.7+), Mutable, Keys are unique, Accessed by key
my_dict = {
    'a': 10,
    'b': 20,
    'c': 20,
    'a': 40   # Duplicate key overrides previous
}

print(my_dict)       # -> {'a': 40, 'b': 20, 'c': 20}
print(my_dict['b'])  # -> 20  (key-based access)
my_dict['c'] = 80    # Update value
print(my_dict)       # -> {'a': 40, 'b': 20, 'c': 80}

# ---------------------------------------
# Access & Checks
# ---------------------------------------

user = {"id": 1, "age": 30, "city": "berlin"}

print(user.get("name", "Unknown"))  # -> Unknown (safe access)

print("age" in user)        # -> True
print("name" not in user)   # -> True

# keys(): Returns a view of all dictionary keys.
print(user.keys())    

# values(): Returns a view of all dictionary values.
print(user.values())  

# items(): Returns key-value pairs as tuples.
print(user.items())   

# ---------------------------------------
# Looping Through Dictionary
# ---------------------------------------
# We can loop by keys or key-value pairs.

user = {"id": 1, "age": 30, "city": "berlin"}

# Loop using keys
for u in user:
    print(u, user[u])

# Loop using items()
for key, value in user.items():
    print(key, value)


# ---------------------------------------
# Add • Update • Remove
# ---------------------------------------

user = {"id": 1, "age": 30, "city": "berlin"}

user["name"] = "John"     # Add new key
user["age"] = 35          # Update value

user.update({"age": 40, "city": "Paris"})  # Update multiple keys
print(user)


# pop(): # Remove a key and return its value.
age = user.pop("salary", "Not Found")  
print(user)
print("Removed Item:", age) 

# popitem(): Remove and return the last inserted pair.
user.popitem() 
print(user)


# ---------------------------------------
# Creating Dictionaries
# ---------------------------------------
# Create dictionary with default values.
user = {
    "id": None,
    "name": None,
    "age": None,
    "city": None
}

# fromkeys(): Create dictionary from a list of keys with same default value.
user = dict.fromkeys(["id", "name", "age", "city"], None)
print(user)

# ---------------------------------------
# Dictionary Comprehension Challenge
# ---------------------------------------
# Goal:
# 1. Keep only pairs where value is a string
# 2. Convert keys to UPPERCASE
# 3. Convert values to lowercase

user = {"id": 1, "name": "John", "age": 30, "city": "Berlin"}

user_str = {
    k.upper(): v.lower()        # Expression (transform)
    for k, v in user.items()    # Loop
    if isinstance(v, str)       # Filter
}

print(user_str)
