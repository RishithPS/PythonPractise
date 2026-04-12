# ================================================================================
# CONDITIONAL STATEMENTS (IF / ELSE / ELIF)
# ----------------------------------------
# Python uses `if`, `elif`, and `else` to control the flow of decisions.
# You can nest conditions or combine them using logical operators.
# ================================================================================

# ---------------------------------------
# Simple If Condition
# ---------------------------------------
score = 100
if score >= 90:
    print("A")

# ---------------------------------------
# If / Else
# ---------------------------------------
score = 50
if score >= 90:
    print("A")
else:
    print("F")

# ---------------------------------------
# If / Elif / Else
# ---------------------------------------
score = 50
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("F")

# ---------------------------------------
# Full Grading Logic with Multiple Elif
# ---------------------------------------
score = 50
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")

# ---------------------------------------
# Nested If: Project Bonus
# ---------------------------------------
score = 50
submitted_project = True

if score >= 90:
    if submitted_project:
        print("A+")
    else:
        print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")

# ---------------------------------------
# Combined Conditions with and/or
# ---------------------------------------
score = 50
submitted_project = True

if score >= 90 and submitted_project:
    print("A+")
elif score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60 or submitted_project:
    print("D")
else:
    print("F")

# ---------------------------------------
# Independent Conditions
# ---------------------------------------
score = 50
submitted_project = True

if score >= 90:
    print("High Score")
else:
    print("Low Score")

if submitted_project:
    print("Project is submitted")
else:
    print("Project is not submitted")
