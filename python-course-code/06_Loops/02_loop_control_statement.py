# ================================================================================
# LOOP CONTROL STATEMENTS
# ----------------------------------------
# Sometimes we don’t want a loop to run normally.
# We may want to stop it early, skip an iteration,
# or simply leave a placeholder for future logic.
#
# In this file, we explore:
# break
# continue
# pass
# for-else
# ================================================================================


# ---------------------------------------
# break
# ---------------------------------------
# The break statement immediately stops the loop when a condition is met.

names = ['john', 'maria', '', 'kumar']

for name in names:
    if name == '':
        print('Empty value detected!')
        break
    print(f'Name = {name}')


# ---------------------------------------
# continue
# ---------------------------------------
# The continue statement skips the current iteration and moves to the next one.

names = ['john', 'maria', '', 'kumar']

for name in names:
    if name == '':
        print('Empty value detected!')
        continue
    print(f'Name = {name}')


# ---------------------------------------
# pass
# ---------------------------------------
# The pass statement does nothing.
# It acts as a placeholder for future code.

names = ['john', 'maria', '', 'kumar']

for name in names:
    if name == '':
        pass  # TODO: Handle Empty Value
        name = name.replace('', 'unknown')
    print(f'Name = {name}')



# TASK
# Loop through a list of days and print. only the working days, skipping weekends.
days = ['Mon', 'Sun', 'Wed', 'Tue']
weekends = ['Sat', 'Sun']

for day in days:
    if day in weekends:
        continue
    print(f'Workday: {day}')


# Real-World Example (Security Check)
# Stop processing if a suspicious input appears.
emails = [
    'data@gmail.com',
    'baraa@outlook.de',
    'DROP TABLE USERS;',
    'maria@gmail.com'
]

for email in emails:
    if ';' in email:
        print('SQL Injection: Hacker Attack')
        break
    print(f'Processing Email: {email}')


# ---------------------------------------
# for-else
# ---------------------------------------
# The else block runs only if the loop completes without hitting break.

items = [1, 3, 4, 7]

for i in items:
    print(i)
else:
    print("Loop is completed")


# Task: Check for Even Number
# If no even number is found,
# the else block will execute.
items = [1, 3, 5, 7]

for i in items:
    if i % 2 == 0:
        print("Even Nr. Found:", i)
        break
else:
    print("All numbers are odd")


# TASK: Check for missing names in a list.
names = ['Kamara', 'Tuba', None, 'Mounika']

for name in names:
    if name is None:
        print("Found a missing name")
        break
else:
    print("All names are available")

# TASK: Check if all files are CSV files.

files = ['data1.csv', 'report.pdf', 'data2.txt', 'report2.csv']

for file in files:
    if not file.endswith('.csv'):
        print(f'{file} is not a CSV')
        break
else:
    print('All files are CSV')


# ---------------------------------------
# Python Challenge
# ---------------------------------------
# Check whether any filename appears more than once.
# Print "Duplicate found" if a duplicate exists,
# otherwise print "All files are unique".

file_list = [
    'report.csv',
    'data.xlsx',
    'summary.docx',
    'report.csv',
    'data.csv'
]

for file in file_list:
    if file_list.count(file) > 1:
        print(f"Duplicate found: {file}")
        break
else:
    print("All files are unique")