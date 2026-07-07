# ==========================================
# Borrow & Return Module
# ==========================================
from utils import print_title, success, error
from datetime import datetime, timedelta
from file_handler import load_data, save_data

BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"
BORROW_FILE = "borrow_records.json"


# ------------------------------------------
# Issue Book
# ------------------------------------------

def issue_book():

    books = load_data(BOOKS_FILE)
    members = load_data(MEMBERS_FILE)
    borrow_records = load_data(BORROW_FILE)

    print_title("ISSUE BOOK")

    member_id = input("Enter Member ID: ")
    book_id = input("Enter Book ID: ")

    # Check Member
    member_found = False

    for member in members:
        if member["member_id"] == member_id:
            member_found = True
            break

    if not member_found:
        error("Member Not Found!")
        return

    # Check Book
    book_found = False

    for book in books:

        if book["book_id"] == book_id:

            book_found = True

            if book["quantity"] <= 0:
                print("Book Not Available!")
                return

            # Reduce Quantity
            book["quantity"] -= 1

            if book["quantity"] == 0:
                book["availability"] = "Not Available"

            borrow_date = datetime.now()

            due_date = borrow_date + timedelta(days=7)

            record = {
                "member_id": member_id,
                "book_id": book_id,
                "borrow_date": borrow_date.strftime("%Y-%m-%d"),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "status": "Borrowed"
            }

            borrow_records.append(record)

            save_data(BOOKS_FILE, books)
            save_data(BORROW_FILE, borrow_records)

            success("Book Issued Successfully!")
            return

    if not book_found:
        error("Book Not Found!")


# ------------------------------------------
# View Borrow Records
# ------------------------------------------

def view_borrow_records():

    records = load_data(BORROW_FILE)

    print("\n===== BORROW RECORDS =====")

    if len(records) == 0:
        print("No Borrow Records Found.")
        return

    for record in records:

        print("-" * 40)

        print("Member ID   :", record["member_id"])
        print("Book ID     :", record["book_id"])
        print("Borrow Date :", record["borrow_date"])
        print("Due Date    :", record["due_date"])
        print("Status      :", record["status"])

    print("-" * 40)

    # ------------------------------------------
# Return Book
# ------------------------------------------

def return_book():

    books = load_data(BOOKS_FILE)
    borrow_records = load_data(BORROW_FILE)

    print("\n===== RETURN BOOK =====")

    member_id = input("Enter Member ID: ")
    book_id = input("Enter Book ID: ")

    for record in borrow_records:

        if (record["member_id"] == member_id and
            record["book_id"] == book_id and
            record["status"] == "Borrowed"):

            record["status"] = "Returned"

            for book in books:

                if book["book_id"] == book_id:

                    book["quantity"] += 1
                    book["availability"] = "Available"

                    break

            save_data(BOOKS_FILE, books)
            save_data(BORROW_FILE, borrow_records)

            success("Book Returned Successfully!")
            return

    print("Borrow Record Not Found!")

    # ------------------------------------------
# Check Overdue Books
# ------------------------------------------

def check_overdue():

    records = load_data(BORROW_FILE)

    print("\n===== OVERDUE BOOKS =====")

    today = datetime.now().date()

    found = False

    for record in records:

        if record["status"] == "Borrowed":

            due_date = datetime.strptime(
                record["due_date"],
                "%Y-%m-%d"
            ).date()

            if today > due_date:

                found = True

                print("-" * 40)
                print("Member ID :", record["member_id"])
                print("Book ID   :", record["book_id"])
                print("Due Date  :", record["due_date"])
                print("Status    : OVERDUE")

    if not found:
        print("No Overdue Books.")

     # ------------------------------------------
# Borrow Menu
# ------------------------------------------

def borrow_menu():

    while True:

        print("\n" + "=" * 60)
        print("            BORROW & RETURN")
        print("=" * 60)

        print("1. Issue Book")
        print("2. Return Book")
        print("3. View Borrow Records")
        print("4. Check Overdue Books")
        print("5. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            issue_book()

        elif choice == "2":
            return_book()

        elif choice == "3":
            view_borrow_records()

        elif choice == "4":
            check_overdue()

        elif choice == "5":
            print("\nReturning to Admin Dashboard...")
            break

        else:
            print("Invalid Choice!")   