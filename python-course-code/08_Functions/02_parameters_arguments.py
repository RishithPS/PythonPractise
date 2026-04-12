# ================================================================================
# FUNCTION PARAMETERS & SCOPE
# ----------------------------------------
# Functions can accept inputs (parameters).
# These inputs allow the function to behave dynamically.
#
# We will explore:
# - Simple parameter usage
# - Global vs local variables
# - Positional arguments
# - Keyword arguments
# - Default parameters
# ================================================================================


# Adding Input
# We pass a name and clean it before printing.

def clean_name(name):
    print(name.strip().lower())

clean_name(" MariA ")   # -> maria
clean_name("KUMAR ")    # -> kumar
clean_name("")          # ->  (empty string remains empty)


# ---------------------------------------
# Parameters vs Global vs Local Variable
# ---------------------------------------
# Global variables exist outside the function.
# Local variables exist only inside the function.

case_rule = "n/a"  # Global variable

def clean_name(name):  # Parameter
    cleaned = name.strip()  # Local variable
    
    if case_rule == "lower":
        cleaned = cleaned.lower()
    
    print("Cleaned:", cleaned)

# print(name) -> Parameters can be accessed only inside functions
# print(cleaned) -> local variables can be accessed only inside functions
clean_name(" MariA ") 
print("The Rule is:", case_rule) 


# -----------------------------------------------------------
# Positional, Keyword, mixed Arguements | Default Parameters
# -----------------------------------------------------------
# Functions can accept multiple inputs.

def clean_name(first_name, last_name, country="n/a"):
    first = first_name.strip().lower()
    last = last_name.strip().lower()
    full_name = first + " " + last
    print(full_name, "From", country)


# Positional Arguments (Access based on order)
clean_name(" MariA ", "SMITH ", "DE")

# Keyword Arguments (Access based on parameter name)
clean_name(country="DE", first_name=" MariA ", last_name="SMITH ")

# Mixed Arguments (Positional first, then keyword)
clean_name(" MariA ", "SMITH ", country="DE")

# Default Parameter (If country not provided, default is used.)
clean_name("Kumar", "Suresh")
