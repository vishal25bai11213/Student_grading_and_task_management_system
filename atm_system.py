# --- Global State ---
users = {}
current_user = None

# --- Menu Functions ---


def print_menu():
    print("\n" + "=" * 40)
    print("ATM MENU")
    print("=" * 40)
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View Transaction History")
    print("5. Logout")
    print("=" * 40)


def print_login_menu():
    print("\n" + "=" * 40)
    print("WELCOME TO ATM SYSTEM")
    print("=" * 40)
    print("1. Login")
    print("2. Create Account")
    print("3. Exit")
    print("=" * 40)

# --- Account Management ---


def create_account():
    print("\n--- CREATE ACCOUNT ---")
    username = input("Enter username: ")

    if username in users:
        print("Username already exists!")
        return

    pin = input("Enter 4-digit PIN: ")

    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be exactly 4 digits!")
        return

    try:
        initial_deposit = float(input("Enter initial deposit: $"))
        if initial_deposit < 0:
            print("Initial deposit cannot be negative!")
            return
    except:
        print("Invalid amount!")
        return

    users[username] = {
        "pin": pin,
        "balance": initial_deposit,
        "transactions": []
    }

    print(f"Account created successfully!")
    print(f"Your balance: ${initial_deposit}")


def login():
    global current_user

    print("\n--- LOGIN ---")
    username = input("Enter username: ")
    pin = input("Enter PIN: ")

    if username in users and users[username]["pin"] == pin:
        current_user = username
        print(f"Welcome back, {username}!")
    else:
        print("Invalid username or PIN!")

# --- Transaction Functions ---


def check_balance():
    balance = users[current_user]["balance"]
    print(f"\nYour balance: ${balance:.2f}")


def deposit():
    try:
        amount = float(input("\nEnter amount to deposit: $"))

        if amount <= 0:
            print("Amount must be positive!")
            return

        users[current_user]["balance"] += amount

        transaction = f"Deposit: ${amount:.2f}"
        users[current_user]["transactions"].append(transaction)

        print(f"Successfully deposited ${amount:.2f}")
        print(f"New balance: ${users[current_user]['balance']:.2f}")

    except:
        print("Invalid amount!")


def withdraw():
    try:
        amount = float(input("\nEnter amount to withdraw: $"))

        if amount <= 0:
            print("Amount must be positive!")
            return

        if amount > users[current_user]["balance"]:
            print("Insufficient funds!")
            return

        users[current_user]["balance"] -= amount

        transaction = f"Withdrawal: ${amount:.2f}"
        users[current_user]["transactions"].append(transaction)

        print(f"Successfully withdrew ${amount:.2f}")
        print(f"New balance: ${users[current_user]['balance']:.2f}")

    except:
        print("Invalid amount!")


def view_history():
    print("\n" + "=" * 40)
    print("TRANSACTION HISTORY")
    print("=" * 40)

    transactions = users[current_user]["transactions"]

    if not transactions:
        print("No transactions yet.")
    else:
        for i, txn in enumerate(transactions, 1):
            print(f"{i}. {txn}")

    print("=" * 40)


def logout():
    global current_user
    print(f"Goodbye, {current_user}!")
    current_user = None

# --- Main Program Loop ---


def main():
    global current_user

    print("=" * 40)
    print("WELCOME TO ATM SIMULATION")
    print("=" * 40)

    while True:
        if current_user is None:
            print_login_menu()
            choice = input("Enter choice: ")

            if choice == "1":
                login()
            elif choice == "2":
                create_account()
            elif choice == "3":
                print("Thank you for using ATM. Goodbye!")
                break
            else:
                print("Invalid choice!")

        else:
            print_menu()
            choice = input("Enter choice: ")

            if choice == "1":
                check_balance()
            elif choice == "2":
                deposit()
            elif choice == "3":
                withdraw()
            elif choice == "4":
                view_history()
            elif choice == "5":
                logout()
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    main()
