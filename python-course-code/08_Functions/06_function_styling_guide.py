x = 10

match x:
    case 1:
        print("One")
    case 2:
        print("Two")
    case _:
        print("Other")

# ================================================================================
# FUNCTION BEST PRACTICES (CLEAN • PROFESSIONAL • READABLE)
# ----------------------------------------
# Writing functions is not just about making them work.
# It is about making them:
# - Readable
# - Maintainable
# - Professional
# ================================================================================


# --------------------------------------
# ❌ Bad Style Example
# ---------------------------------------
# Problems:
# - Not snake_case
# - Unclear parameter names
# - Prints inside function
# - Modifies input parameter
# - No docstring
# - No type hints

def DiscPrint(p, r):
    print("calculating discount")
    p = p - (p * r / 100)
    print(p)

DiscPrint(80, 20)


# ---------------------------------------
# ✅ Professional Style Version
# ---------------------------------------

def calculate_discount(price: float, discount_rate: float) -> float:
    """
    Calculate the final price after applying a discount.

    Args:
        price (float): Original product price.
        discount_rate (float): Discount rate as percentage (e.g., 20 for 20%).

    Returns:
        float: Final price after applying the discount.
    """

    final_price = price - (price * discount_rate / 100)
    return final_price


print("Calculating Discount")

result = calculate_discount(80, 20)

print(result)  # -> 64.0


# ---------------------------------------
# Best Practice Rules Summary
# ---------------------------------------
# 1. Use snake_case for function names.
# 2. Start function names with a clear verb (calculate, get, load, validate).
# 3. Use descriptive parameter names (price, discount_rate).
# 4. Always add a docstring.
# 5. Return values instead of printing inside functions.
# 6. Do not modify input parameters.
# 7. Add type hints for clarity.
# 8. Document inputs and outputs clearly.
