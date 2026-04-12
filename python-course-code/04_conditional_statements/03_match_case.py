# ================================================================================
# MATCH-CASE (STRUCTURAL PATTERN MATCHING)
# ----------------------------------------
# Introduced in Python 3.10.
#
# match-case is cleaner than multiple if-elif
# when checking many possible values.
# ================================================================================


# ---------------------------------------
# Traditional If-Elif Version
# ---------------------------------------

country = "USA"

if country == "United States":
    print("US")
elif country == "India":
    print("IN")
elif country == "Egypt":
    print("EG")
elif country == "Germany":
    print("DE")
else:
    print("Unknown Country")


# ---------------------------------------
# match-case Version
# ---------------------------------------
# Cleaner and more readable for many conditions.

country = "USA"

match country:

    case "United States" | "USA":
        print("US")

    case "India":
        print("IN")

    case "Egypt":
        print("EG")

    case "Germany":
        print("DE")

    case _:
        print("Unknown Country")


# Example 2: HTTP Status Handler
# Handle response codes from an API.

status_code = 404

match status_code:

    case 200:
        print("Request successful")

    case 400:
        print("Bad request")

    case 401:
        print("Unauthorized access")

    case 404:
        print("Resource not found")

    case 500:
        print("Internal server error")

    case _:
        print("Unhandled status code")