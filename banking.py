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

class account():
    def __init__(self, name = "", email = "", password = "", balance = "0"):
        self._name = name
        self._email = email
        self._password = password
        self._balance = balance

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, val):
        while True:
            self._name = input("Enter your name: ")
            if not is_valid_name(self._name):
                print("Invalid name format. Please try again.")
            else:
                break
        
    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, val):
        while True:
            self._email = input("Enter your email: ")
            if not is_valid_email(self._email):
                print("Invalid email format. Please try again.")
            elif self.check_duplicate_email(self._email):
                print("An account with this email already exists. Please use a different email.")
            else:
                break
        
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, val):
        while True:
            self._password = input("Create a password: ")
            if not is_valid_password(self._password):
                print("Invalid password format. Please try again.")
            else:
                break

    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, val):
        self._balance = val

    def __str__(self):
        return f"Name: {self._name} | Email: {self._email}"
    
    def get_balance(self):
        print(f"Your account balance: ${self._balance}")

    def check_duplicate_email(self, email):
        with open("bank_accounts.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == email:
                    return True
        return False

class bank():
    def create_account(self, act):
        with open("bank_accounts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([act.name, act.email, act.password, act.balance])
            print("Account successfully created")

    def update_account(self, act):
        with open("bank_accounts.csv", "r") as file:
            lines = file.readlines()

        with open("bank_accounts.csv", "w") as file:
            writer = csv.writer(file)
            for line in lines:
                email = list(map(str, line.split(",")))[1]
                if email == act.email:
                    writer.writerow([act.name, act.email, act.password, act.balance])
                else:
                    writer.writerow(line.strip().split(","))
    
    def login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        with open("bank_accounts.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == email and row[2] == password:
                    act = account(row[0], row[1], row[2], row[3])
                    return act
        return None
    
    def deposit(self, act):
        while True:
            amount = input("Enter the amount to deposit: ")
            if not is_valid_amount(amount):
                print("Invalid amount. Amount must be a number greater than 0.")
            else:
                act.balance = str(int(act.balance) + int(amount))
                self.update_account(act)
                print("Deposit successful.")
                break

    def withdraw(self, act):
        while True:
            amount = input("Enter the amount to withdraw: ")
            if not is_valid_amount(amount):
                print("Invalid amount. Amount must be a number greater than 0.")
            elif int(amount) > int(act.balance):
                print("Insufficient balance.")
            else:
                act.balance = str(int(act.balance) - int(amount))
                self.update_account(act)
                print("Withdrawal successful.")
                break


def main():
    BANK = bank()
    while True:
        print("\n1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        match choice:
            case "1":
                ACCOUNT = account()
                ACCOUNT.name = ""
                ACCOUNT.email = ""
                ACCOUNT.password = ""
                BANK.create_account(ACCOUNT)
            case "2":
                ACCOUNT = BANK.login()
                if ACCOUNT:
                    print(f"Welcome, {ACCOUNT.name}!")
                    while True:
                        print("\n1. Deposit")
                        print("2. Withdraw")
                        print("3. Check Balance")
                        print("4. Logout")
                        sub_choice = input("Enter your choice: ")

                        match sub_choice:
                            case "1":
                                BANK.deposit(ACCOUNT)
                            case "2":
                                BANK.withdraw(ACCOUNT)
                            case "3":
                                ACCOUNT.get_balance()
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
