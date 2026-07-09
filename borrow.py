# ==========================================
# Borrow & Return Module
# ==========================================
from utils import print_title, success, error
from datetime import datetime, timedelta
from file_handler import load_data, save_data

BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"
BORROW_FILE = "borrow_records.json"
BORROW_LIMIT = 3


# ------------------------------------------
# Issue Book
# ------------------------------------------

# ------------------------------------------
# Issue Book
# ------------------------------------------

def issue_book(prefilled_member_id=None):

    books = load_data(BOOKS_FILE)
    members = load_data(MEMBERS_FILE)
    borrow_records = load_data(BORROW_FILE)

    print_title("ISSUE BOOK")

    # If member_id is passed from dashboard, use it; otherwise, ask for input
    if prefilled_member_id:
        member_id = prefilled_member_id
    else:
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

    # Enforce borrow limit per member
    current_borrowed = 0

    for r in borrow_records:
        if r.get("member_id") == member_id and r.get("status") == "Borrowed":
            current_borrowed += 1

    if current_borrowed >= BORROW_LIMIT:
        print(f"Member has reached the borrow limit ({BORROW_LIMIT}). Return a book before issuing another.")
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
# Return Book
# ------------------------------------------

def return_book(prefilled_member_id=None):

    books = load_data(BOOKS_FILE)
    borrow_records = load_data(BORROW_FILE)

    print("\n===== RETURN BOOK =====")

    # Use prefilled ID if available
    if prefilled_member_id:
        member_id = prefilled_member_id
    else:
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


def view_member_borrow_records(member_id):

    records = load_data(BORROW_FILE)

    print(f"\n===== BORROW RECORDS FOR {member_id} =====")

    found = False

    for record in records:

        if record["member_id"] == member_id:

            found = True

            print("-" * 40)
            print("Member ID   :", record["member_id"])
            print("Book ID     :", record["book_id"])
            print("Borrow Date :", record["borrow_date"])
            print("Due Date    :", record["due_date"])
            print("Status      :", record["status"])

    if not found:
        print("No Borrow Records Found for this member.")

    print("-" * 40)

    # ------------------------------------------
# Return Book
# ------------------------------------------

def return_book(prefilled_member_id=None):

    books = load_data(BOOKS_FILE)
    borrow_records = load_data(BORROW_FILE)

    print("\n===== RETURN BOOK =====")

    # Use prefilled ID if available
    if prefilled_member_id:
        member_id = prefilled_member_id
    else:
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
    try:
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

    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted. Returning to Admin Dashboard...")
        return