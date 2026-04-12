# ================================================================================
# WHILE LOOP
# ----------------------------------------
# A while loop runs as long as a condition is True.
# Unlike the for loop, we do not iterate over a collection.
# Instead, we control the loop using a condition.
#
# It is commonly used when:
# - We do not know how many times the loop should run
# - We wait for user input
# - We repeat until a condition changes
# ================================================================================


# ---------------------------------------
# Basic While Loop
# ---------------------------------------
# The loop runs while the condition is True.
# We must manually update the variable to avoid an infinite loop.

count = 1

while count <= 10:
    print(count)
    count += 2


# TASK: Keep asking the user "Do you agree?" until the user types "yes"
answer = ""

while answer != "yes":
    answer = input("Do you agree? (yes/no): ")

print("Thank You")


# ---------------------------------------
# While True + break
# ---------------------------------------
# Another common pattern.
# The loop runs forever until we explicitly break it.

while True:
    answer = input("Do you agree? (yes/no): ")
    
    if answer == "yes":
        break

print("Thank You")


# ---------------------------------------
# While Else Break
# ---------------------------------------
# The else block runs only if the loop
# finishes without hitting break.

attempts = 0

while attempts < 3:
    answer = input("Do you agree? (yes/no): ")
    
    if answer == "yes":
        print("Glad we're on the same page")
        break
    
    attempts += 1
else:
    print("3 strikes. You're out!")