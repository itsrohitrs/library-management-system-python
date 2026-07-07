# ==========================================
# Book Management Module
# ==========================================
from utils import print_title, success, error, get_integer, not_empty
from file_handler import load_data, save_data

BOOKS_FILE = "books.json"


# ------------------------------------------
# Add Book
# ------------------------------------------

def add_book():

    books = load_data(BOOKS_FILE)

    print_title("ADD BOOK")

    book_id = not_empty("Enter Book ID: ")

    # Duplicate Book ID Check
    for book in books:
        if book["book_id"] == book_id:
            print("Book ID already exists!")
            return

    title = not_empty("Enter Title: ")
    author = not_empty("Enter Author: ")
    genre = not_empty("Enter Genre: ")

    while True:
        try:
            quantity = get_integer("Enter Quantity: ")

            if quantity < 0:
                print("Quantity cannot be negative.")
            else:
                break

        except ValueError:
            print("Please enter a valid number.")

    availability = "Available"

    if quantity == 0:
        availability = "Not Available"

    new_book = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "genre": genre,
        "quantity": quantity,
        "availability": availability
    }

    books.append(new_book)

    save_data(BOOKS_FILE, books)

    success("Book Added Successfully!")


# ------------------------------------------
# View All Books
# ------------------------------------------

def view_books():

    books = load_data(BOOKS_FILE)

    print("\n===== ALL BOOKS =====")

    if len(books) == 0:
        print("No Books Available.")
        return

    for book in books:

        print("-" * 40)

        print("Book ID      :", book["book_id"])
        print("Title        :", book["title"])
        print("Author       :", book["author"])
        print("Genre        :", book["genre"])
        print("Quantity     :", book["quantity"])
        print("Availability :", book["availability"])

    print("-" * 40)


# ------------------------------------------
# Search Book
# ------------------------------------------

def search_book():

    books = load_data(BOOKS_FILE)

    print("\n===== SEARCH BOOK =====")

    search_id = input("Enter Book ID: ")

    for book in books:

        if book["book_id"] == search_id:

            print("\nBook Found")

            print("Book ID      :", book["book_id"])
            print("Title        :", book["title"])
            print("Author       :", book["author"])
            print("Genre        :", book["genre"])
            print("Quantity     :", book["quantity"])
            print("Availability :", book["availability"])

            return

    error("Book Not Found!")

    # ------------------------------------------
# Update Book
# ------------------------------------------

def update_book():

    books = load_data(BOOKS_FILE)

    print("\n===== UPDATE BOOK =====")

    book_id = input("Enter Book ID to Update: ")

    for book in books:

        if book["book_id"] == book_id:

            book["title"] = input("Enter New Title: ")
            book["author"] = input("Enter New Author: ")
            book["genre"] = input("Enter New Genre: ")

            while True:

                try:
                    quantity = int(input("Enter New Quantity: "))

                    if quantity < 0:
                        print("Quantity cannot be negative.")

                    else:
                        break

                except ValueError:
                    print("Enter a valid number.")

            book["quantity"] = quantity

            if quantity > 0:
                book["availability"] = "Available"
            else:
                book["availability"] = "Not Available"

            save_data(BOOKS_FILE, books)

            print("\nBook Updated Successfully!")

            return

    print("Book Not Found!")


# ------------------------------------------
# Delete Book
# ------------------------------------------

def delete_book():

    books = load_data(BOOKS_FILE)

    print("\n===== DELETE BOOK =====")

    book_id = input("Enter Book ID to Delete: ")

    for book in books:

        if book["book_id"] == book_id:

            books.remove(book)

            save_data(BOOKS_FILE, books)

            print("\nBook Deleted Successfully!")

            return

    print("Book Not Found!")


# ------------------------------------------
# Book Management Menu
# ------------------------------------------

def book_menu():

    while True:

        print("\n" + "=" * 60)
        print("               BOOK MANAGEMENT")
        print("=" * 60)

        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            update_book()

        elif choice == "5":
            delete_book()

        elif choice == "6":
            print("Returning to Admin Dashboard...")
            break

        else:
            print("Invalid Choice!")