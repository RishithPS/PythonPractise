# ================================================================================
# NESTED LOOPS
# ----------------------------------------
# A nested loop is a loop inside another loop.
# The inner loop runs completely for every iteration
# of the outer loop.
#
# Nested loops are commonly used for:
# - Combinations
# - Data generation
# - Matrix-like structures
# - Query building
# ================================================================================


# ---------------------------------------
# Nested Loop (2 Levels)
# ---------------------------------------
for x in range(3):  # outer loop
    for y in range(2):  # inner loop
        print(f"({x}, {y})")


# ---------------------------------------
# Nested Loop (3 Levels)
# ---------------------------------------
for x in range(3):  # outer loop
    for y in range(2):  # inner loop
        for z in range(2):
            print(f"({x}, {y}, {z})")

# ---------------------------------------
# Combination Example
# ---------------------------------------
# Generating combinations of colors and sizes.

colors = ['red', 'blue', 'green']
sizes = ['L', 'M', 'S']

for color in colors:
    for size in sizes:
        print(f'{color} - Size {size}')


# ---------------------------------------
# Real-World Example (File Generation)
# ---------------------------------------
# Generating file names dynamically using years, months, and days.

years = [2026, 2027]
months = ['Jan', 'Feb']
days = range(1, 29)

for y in years:
    for m in months:
        for d in days:
            print(f'report_{y}_{m}_{d}.csv')


# ---------------------------------------
# Real-World Example (SQL Generation)
# ---------------------------------------
# Automatically generating SQL queries for multiple tables and columns.

tables = ['customers', 'orders', 'products', 'prices']
columns = ['id', 'create_date']

for t in tables:
    for c in columns:
        print(f'SELECT count(*) FROM {t} WHERE {c} IS NULL;')