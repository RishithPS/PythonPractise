# ================================================================================
# FUNCTION TYPES (ACTION • TRANSFORMATION • VALIDATION • ORCHESTRATION)
# ----------------------------------------
# Not all functions are the same.
#
# In real projects, we usually create:
# - Action Functions         → perform an action
# - Transformation Functions → return modified data
# - Validation Functions     → return True / False
# - Orchestrator Functions   → control program flow
# ================================================================================


# ---------------------------------------
# ACTION FUNCTION
# ---------------------------------------
# Task: Store application log messages in a file.
# Action functions usually do something,
# but they do NOT return a value.

def write_log(message):
    with open(r"C:\Main\Python\app.log", "a") as file:
        file.write(message + "\n")

#write_log("App Started")
#write_log("User logged in")
#write_log("App Stopped")


# ---------------------------------------
# TRANSFORMATION FUNCTION
# ---------------------------------------
# Task: Clean an email and split it into username and domain.
# Transformation functions return structured data.

def clean_and_split_email(email):
    cl_email = email.strip().lower()
    username, domain = cl_email.split("@")

    return {
        "username": username,
        "domain": domain
    }

print(clean_and_split_email(" SARA@gmAil.com "))

# ---------------------------------------
# VALIDATION FUNCTION
# ---------------------------------------
# Task: Basic email validation.

def is_valid_email(email):
    return "@" in email and "." in email

print(is_valid_email("saragmail.com"))     # -> False
print(is_valid_email("sara@gmail.com"))    # -> True
print(is_valid_email("sara@gmailcom"))     # -> False
print(is_valid_email("saragmailcom"))      # -> False

# ---------------------------------------
# ORCHESTRATION FUNCTION (Mini Project)
# ---------------------------------------
# Project Flow:
# 1. Receive email
# 2. Validate email
# 3. If invalid → log error
# 4. If valid → clean & structure email
# 5. Log each step


def process_user_email(email):

    write_log("App Started")

    if not is_valid_email(email):
        write_log(f"Invalid Email received: {email}")

    else:
        clean_email = clean_and_split_email(email)
        write_log(f"Processed Email: {clean_email}")

    write_log("App Stopped")


# Receive input from user
email = input("Please enter your Email: ")
process_user_email(email)