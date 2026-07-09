# ==========================================
# Library Management System
# ==========================================

from auth import register, login
from books import book_menu, view_books, search_book
from members import member_menu
from borrow import borrow_menu, view_member_borrow_records, issue_book, return_book
from users import user_menu


def admin_dashboard():
    try:
        while True:

            print("\n" + "=" * 60)
            print("              ADMIN DASHBOARD")
            print("=" * 60)

            print("1. Book Management")
            print("2. Member Management")
            print("3. Borrow & Return")
            print("4. User Management")
            print("5. Logout")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                book_menu()

            elif choice == "2":
                member_menu()

            elif choice == "3":
                borrow_menu()

            elif choice == "4":
                user_menu()

            elif choice == "5":
                print("\nLogged Out Successfully!")
                break

            else:
                print("Invalid Choice!")

    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted. Returning to main menu...")
        return


def main():
    try:
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
                    if user.get("role") == "Admin":
                        admin_dashboard()
                    else:
                        # Member dashboard: ask for member_id to associate
                        print("\nLogged in as Member.")

                        member_id = input("Enter your Member ID to continue: ")

                        # Basic check: ensure member exists in members.json
                        from file_handler import load_data

                        members = load_data("members.json")

                        found = False

                        for m in members:
                            if m.get("member_id") == member_id:
                                found = True
                                break

                        if not found:
                            print("Member record not found. Please ask admin to register you as a member.")
                        else:
                            # Member menu loop
                            try:
                                while True:
                                    print("\n" + "=" * 60)
                                    print("               MEMBER DASHBOARD")
                                    print("=" * 60)

                                    print("1. View All Books")
                                    print("2. Search Book")
                                    print("3. Issue Book")
                                    print("4. Return Book")
                                    print("5. View My Borrow Records")
                                    print("6. Logout")

                                    ch = input("\nEnter your choice: ")

                                    if ch == "1":
                                        view_books()

                                    elif ch == "2":
                                        search_book()

                                    elif ch == "3":
                                        # reuse existing issue flow but prefill member id
                                        print("Issuing book for Member ID:", member_id)
                                        issue_book(prefilled_member_id=member_id)

                                    elif ch == "4":
                                        print("Returning book for Member ID:", member_id)
                                        return_book(prefilled_member_id=member_id)

                                    elif ch == "5":
                                        view_member_borrow_records(member_id)

                                    elif ch == "6":
                                        print("\nLogged Out Successfully!")
                                        break

                                    else:
                                        print("Invalid Choice!")

                            except (EOFError, KeyboardInterrupt):
                                print("\nInput interrupted. Returning to main menu...")

            elif choice == "3":

                print("Thank You for using Library Management System.")
                break

            else:

                print("Invalid Choice!")

    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted. Exiting program.")
        return


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram interrupted. Exiting.")