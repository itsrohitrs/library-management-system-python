# ==========================================
# Library Management System
# ==========================================

from auth import register, login
from books import book_menu
from members import member_menu
from borrow import borrow_menu


def admin_dashboard():

    while True:

        print("\n" + "=" * 60)
        print("              ADMIN DASHBOARD")
        print("=" * 60)

        print("1. Book Management")
        print("2. Member Management")
        print("3. Borrow & Return")
        print("4. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            book_menu()

        elif choice == "2":
            member_menu()

        elif choice == "3":
            borrow_menu()

        elif choice == "4":
            print("\nLogged Out Successfully!")
            break

        else:
            print("Invalid Choice!")


def main():

    while True:

        print("\n" + "=" * 60)
        print("          LIBRARY MANAGEMENT SYSTEM")
        print("=" * 60)

        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            register()

        elif choice == "2":

            user = login()

            if user:
                admin_dashboard()

        elif choice == "3":

            print("Thank You for using Library Management System.")
            break

        else:

            print("Invalid Choice!")


if __name__ == "__main__":
    main()