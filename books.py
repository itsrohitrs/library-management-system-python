from file_handler import load_data, save_data

BOOKS_FILE = "books.json"

def add_book(book_id, title, author, genre, quantity):
    """
    Creates a new book record. Enforces unique Book ID validation
    and initializes tracking counters.
    """
    if not book_id or not title or not author or not genre:
        return False, "All fields are required."
    
    try:
        quantity = int(quantity)
        if quantity < 0:
            return False, "Quantity cannot be negative."
    except ValueError:
        return False, "Quantity must be a valid number."

    books = load_data(BOOKS_FILE)
    
    # Check for Duplicate Book ID
    for book in books:
        if book['book_id'].strip().lower() == book_id.strip().lower():
            return False, f"Duplicate Error: Book ID '{book_id}' already exists."

    new_book = {
        "book_id": book_id.strip(),
        "title": title.strip(),
        "author": author.strip(),
        "genre": genre.strip(),
        "quantity": quantity,
        "available": quantity  # Initially, all copies are available to borrow
    }
    
    books.append(new_book)
    save_data(BOOKS_FILE, books)
    return True, f"Book '{title}' successfully added to the catalog."

def view_all_books():
    """
    Returns the complete array of books.
    """
    return load_data(BOOKS_FILE)

def search_books(query, search_by="title"):
    """
    Reads the dataset and returns books that partially match the search query.
    search_by can be 'title', 'author', or 'genre'.
    """
    books = load_data(BOOKS_FILE)
    results = []
    query = query.strip().lower()
    
    for book in books:
        if query in book.get(search_by, "").lower():
            results.append(book)
            
    return results

def update_book(book_id, title=None, author=None, genre=None, quantity=None):
    """
    Updates specific attributes of an existing book by its unique ID.
    """
    books = load_data(BOOKS_FILE)
    found = False
    
    for book in books:
        if book['book_id'].strip().lower() == book_id.strip().lower():
            found = True
            if title: book['title'] = title.strip()
            if author: book['author'] = author.strip()
            if genre: book['genre'] = genre.strip()
            if quantity is not None:
                try:
                    qty = int(quantity)
                    if qty < 0:
                        return False, "Quantity cannot be negative."
                    # Adjust availability based on the difference in total quantity
                    diff = qty - book['quantity']
                    book['quantity'] = qty
                    book['available'] = max(0, book['available'] + diff)
                except ValueError:
                    return False, "Quantity must be a valid number."
            break
            
    if not found:
        return False, f"Book ID '{book_id}' not found."
        
    save_data(BOOKS_FILE, books)
    return True, f"Book ID '{book_id}' successfully updated."

def delete_book(book_id):
    """
    Removes a book entirely from the storage registry.
    """
    books = load_data(BOOKS_FILE)
    initial_count = len(books)
    
    # Filter out the book to delete it
    books = [b for b in books if b['book_id'].strip().lower() != book_id.strip().lower()]
    
    if len(books) == initial_count:
        return False, f"Book ID '{book_id}' not found."
        
    save_data(BOOKS_FILE, books)
    return True, f"Book ID '{book_id}' successfully removed from the system."