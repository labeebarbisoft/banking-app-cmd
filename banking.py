import csv
import os
import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_name(name):
    return re.match(r"^(?=.*[A-Za-z])[A-Za-z\s]+$", name)

def is_valid_password(password):
    return len(password) > 0 and password.count(' ') == 0

def is_valid_amount(amount):
    try:
        amount = int(amount)
        return amount > 0
    except:
        return False

def create_account():
    name, email, password = "", "", ""
    while True:
        name = input("Enter your name: ")
        if not is_valid_name(name):
            print("Invalid name format. Please try again.")
        else:
            break
        
    while True:
        email = input("Enter your email: ")
        if not is_valid_email(email):
            print("Invalid email format. Please try again.")
        elif check_duplicate_email(email):
            print("An account with this email already exists. Please use a different email.")
        else:
            break

    while True:
        password = input("Create a password: ")
        if not is_valid_password(password):
            print("Invalid password format. Please try again.")
        else:
            break
    
    balance = 0

    with open("bank_accounts.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, email, password, balance])
        print("Account successfully created")

def check_duplicate_email(email):
    with open("bank_accounts.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == email:
                return True
    return False

def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    with open("bank_accounts.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == email and row[2] == password:
                return row
    return None

def deposit(account):
    while True:
        amount = input("Enter the amount to deposit: ")
        if not is_valid_amount(amount):
            print("Invalid amount. Amount must be a number greater than 0.")
        else:
            account[3] = str(int(account[3]) + int(amount))
            update_account(account)
            print("Deposit successful.")
            break

def withdraw(account):
    while True:
        amount = input("Enter the amount to withdraw: ")
        if not is_valid_amount(amount):
            print("Invalid amount. Amount must be a number greater than 0.")
        elif int(amount) > int(account[3]):
            print("Insufficient balance.")
        else:
            account[3] = str(int(account[3]) - int(amount))
            update_account(account)
            print("Withdrawal successful.")
            break

def check_balance(account):
    print(f"Your account balance: ${account[3]}")

def update_account(account):
    with open("bank_accounts.csv", "r") as file:
        lines = file.readlines()

    with open("bank_accounts.csv", "w") as file:
        writer = csv.writer(file)
        for line in lines:
            email = list(map(str, line.split(",")))[1]
            if email == account[1]:
                writer.writerow(account)
            else:
                writer.writerow(line.strip().split(","))

def main():
    while True:
        print("\n1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        match choice:
            case "1":
                create_account()
            case "2":
                account = login()
                if account:
                    print(f"Welcome, {account[0]}!")
                    while True:
                        print("\n1. Deposit")
                        print("2. Withdraw")
                        print("3. Check Balance")
                        print("4. Logout")
                        sub_choice = input("Enter your choice: ")

                        match sub_choice:
                            case "1":
                                deposit(account)
                            case "2":
                                withdraw(account)
                            case "3":
                                check_balance(account)
                            case "4":
                                print("Logging out.")
                                break
                            case _:
                                print("Invalid choice. Please try again.")
                else:
                    print("Login failed. Please check your email and password.")
            case "3":
                print("Exiting the banking app.")
                break
            case _:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
