import csv
import re

# from menu_constants import (
#     OPEN_ACCOUNT,
#     LOGIN,
#     MAIN_EXIT,
#     DEPOSIT,
#     WITHDRAW,
#     CHECK_BALANCE,
#     SUB_EXIT,
# )


class Menus:
    @staticmethod
    def display_main_menu():
        print("\n1. Open Account")
        print("2. Login")
        print("3. Exit")

    @staticmethod
    def display_sub_menu():
        print("\na. Deposit")
        print("b. Withdraw")
        print("c. Check Balance")
        print("d. Logout")


class Controller:
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_valid_name(name):
        return re.match(r"^(?=.*[A-Za-z])[A-Za-z\s]+$", name)

    def is_valid_password(password):
        return len(password) > 0 and password.count(" ") == 0

    @staticmethod
    def get_valid_name():
        while True:
            name = input("Enter your name: ")
            if not Controller.is_valid_name(name):
                print("Invalid name format. Please try again.")
            else:
                return name

    @staticmethod
    def get_valid_email():
        while True:
            email = input("Enter your email: ")
            if not Controller.is_valid_email(email):
                print("Invalid email format. Please try again.")
            elif DataReader.duplicate_email_exists(email):
                print(
                    "An account with this email already exists. Please use a different email."
                )
            else:
                return email

    @staticmethod
    def get_valid_password():
        while True:
            password = input("Create a password: ")
            if not Controller.is_valid_password(password):
                print("Invalid password format. Please try again.")
            else:
                return password

    @staticmethod
    def get_valid_integer():
        while True:
            try:
                amount = int(input("Enter amount: "))
                if amount > 0:
                    return amount
                else:
                    print("Invalid amount. Please try again.")
            except:
                print("Invalid amount. Please try again.")


class User:
    def __init__(self, name=None, email=None, password=None, balance=None):
        if name is None:
            self.name = Controller.get_valid_name()
        else:
            self.name = name

        if email is None:
            self.email = Controller.get_valid_email()
        else:
            self.email = email

        if password is None:
            self.password = Controller.get_valid_password()
        else:
            self.password = password

        if balance is None:
            self.balance = 0
        else:
            self.balance = balance


class DataReader:
    user_data = [
        {
            "name": "ali",
            "email": "ali@gmail.com",
            "password": "ali",
            "balance": 1000,
        },
        {
            "name": "asad",
            "email": "asad@gmail.com",
            "password": "asad",
            "balance": 1500,
        },
    ]

    @staticmethod
    def duplicate_email_exists(email):
        for user in DataReader.user_data:
            if user["email"] == email:
                return True
        return False

    @staticmethod
    def get_logged_in_user(email, password):
        for user in DataReader.user_data:
            if user["email"] == email and user["password"] == password:
                logged_in_user = User(user["name"], email, password, user["balance"])
                return logged_in_user
        return None

    @staticmethod
    def add_new_user(user):
        DataReader.user_data.append(
            {
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "balance": user.balance,
            }
        )

    @staticmethod
    def update_user_balance(email, new_balance):
        for user in DataReader.user_data:
            if user["email"] == email:
                user["balance"] = new_balance


class Bank:
    @staticmethod
    def create_account():
        user = User()
        DataReader.add_new_user(user)

    @staticmethod
    def login():
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        user = DataReader.get_logged_in_user(email, password)
        return user

    @staticmethod
    def update_account(email, new_balance):
        DataReader.update_user_balance(email, new_balance)

    @staticmethod
    def deposit(user):
        amount = Controller.get_valid_integer()
        user.balance += amount
        Bank.update_account(user.email, user.balance)
        print("Deposit successful.")

    @staticmethod
    def withdraw(user):
        amount = Controller.get_valid_integer()
        if amount > user.balance:
            print("Not enough balance")
        else:
            user.balance -= amount
            Bank.update_account(user.email, user.balance)
            print("Withdraw successful")


def main():
    while True:
        Menus.display_main_menu()
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                Bank.create_account()
            case "2":
                user = Bank.login()
                if user is not None:
                    print(f"Welcome, {user.name}!")
                    while True:
                        Menus.display_sub_menu()
                        sub_choice = input("Enter your choice: ")
                        match sub_choice:
                            case "a":
                                Bank.deposit(user)
                            case "b":
                                Bank.withdraw(user)
                            case "c":
                                print(f"Your balance is : ${user.balance}")
                            case "d":
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
