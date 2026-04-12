"""
Mini Banking System

A simple banking system that allows:
- Account creation
- Deposits
- Withdrawals
- Transaction tracking
- Account summary display
"""


# -------------------------------------------------
# Simulated Database
# -------------------------------------------------

accounts = []


# -------------------------------------------------
# Helper Function: Find Account
# -------------------------------------------------

def find_account(name: str):
    """
    Find an account by name.

    Args:
        name (str): Account holder name.

    Returns:
        dict: Account dictionary if found.
        None: If account does not exist.
    """
    for account in accounts:
        if account["name"].lower() == name.lower():
            return account
    return None


# -------------------------------------------------
# Create Account
# -------------------------------------------------

def create_account(name: str, initial_balance: float):
    """
    Create a new bank account.

    Args:
        name (str): Account holder name.
        initial_balance (float): Starting balance.

    Returns:
        dict: Created account dictionary.

    Raises:
        ValueError: If balance is negative or account exists.
    """
    if initial_balance < 0:
        raise ValueError("Initial balance cannot be negative.")

    if find_account(name):
        raise ValueError("Account with this name already exists.")

    account = {
        "name": name,
        "balance": initial_balance,
        "transactions": []
    }

    accounts.append(account)
    return account


# -------------------------------------------------
# Deposit
# -------------------------------------------------

def deposit(name: str, amount: float):
    """
    Deposit money into an account.

    Args:
        name (str): Account holder name.
        amount (float): Amount to deposit.

    Returns:
        float: Updated balance.

    Raises:
        ValueError: If amount is invalid or account not found.
    """
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than 0.")

    account = find_account(name)

    if not account:
        raise ValueError("Account not found.")

    account["balance"] += amount

    account["transactions"].append({
        "type": "Deposit",
        "amount": amount
    })

    return account["balance"]


# -------------------------------------------------
# Withdraw
# -------------------------------------------------

def withdraw(name: str, amount: float):
    """
    Withdraw money from an account.

    Args:
        name (str): Account holder name.
        amount (float): Amount to withdraw.

    Returns:
        float: Updated balance.

    Raises:
        ValueError: If insufficient funds or invalid amount.
    """
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than 0.")

    account = find_account(name)

    if not account:
        raise ValueError("Account not found.")

    if amount > account["balance"]:
        raise ValueError("Insufficient funds.")

    account["balance"] -= amount

    account["transactions"].append({
        "type": "Withdrawal",
        "amount": amount
    })

    return account["balance"]


# -------------------------------------------------
# Show Account Summary
# -------------------------------------------------

def show_account(name: str):
    """
    Display account summary including transactions.

    Args:
        name (str): Account holder name.
    """
    account = find_account(name)

    if not account:
        print("Account not found.")
        return

    print(f"\nAccount Summary for {account['name']}")
    print(f"Current Balance: ${account['balance']}")

    print("Transactions:")
    if not account["transactions"]:
        print("No transactions yet.")
    else:
        for transaction in account["transactions"]:
            print(f"- {transaction['type']} : ${transaction['amount']}")


# -------------------------------------------------
# Testing Section
# -------------------------------------------------

def run_tests():
    try:
        create_account("Baraa", 1000)
        deposit("Baraa", 200)
        withdraw("Baraa", 150)
        withdraw("Baraa", 2000)  # Overdraft test

    except ValueError as error:
        print("Error:", error)

    show_account("Baraa")


run_tests()