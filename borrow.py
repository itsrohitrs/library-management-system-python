from datetime import datetime, timedelta
from file_handler import load_data, save_data

BORROW_FILE = "borrow_records.json"
BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"

def issue_book(member_id, book_id):
    """
    Issues a book to a member. Checks record existence, validates stock availability,
    decrements count, and saves a 14-day due date transaction.
    """
    books = load_data(BOOKS_FILE)
    members = load_data(MEMBERS_FILE)
    records = load_data(BORROW_FILE)
    
    # 1. Validate Member Existence
    member_exists = any(m['member_id'].strip().lower() == member_id.strip().lower() for m in members)
    if not member_exists:
        return False, f"Transaction Error: Member ID '{member_id}' does not exist."
        
    # 2. Find and Validate Book Availability
    target_book = None
    for b in books:
        if b['book_id'].strip().lower() == book_id.strip().lower():
            target_book = b
            break
            
    if not target_book:
        return False, f"Transaction Error: Book ID '{book_id}' does not exist."
        
    if target_book['available'] <= 0:
        return False, f"Transaction Error: '{target_book['title']}' is currently out of stock."
        
    # 3. Check if this member already has an active borrow record for this exact book
    for r in records:
        if (r['member_id'].strip().lower() == member_id.strip().lower() and 
            r['book_id'].strip().lower() == book_id.strip().lower() and 
            r['return_date'] is None):
            return False, "Transaction Error: This member has already borrowed a copy of this book."

    # 4. Process Inventory Alteration
    target_book['available'] -= 1
    
    # 5. Build Log Transaction
    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=14)
    
    new_record = {
        "record_id": f"REC{len(records) + 1:04d}",
        "member_id": member_id.strip(),
        "book_id": book_id.strip(),
        "issue_date": issue_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "return_date": None
    }
    
    records.append(new_record)
    
    # Save both inventory and transaction tables
    save_data(BOOKS_FILE, books)
    save_data(BORROW_FILE, records)
    return True, f"Success: Book '{target_book['title']}' issued to Member ID '{member_id}'. Due date: {new_record['due_date']}."

def return_book(member_id, book_id):
    """
    Returns an issued book. Restores available stock count and logs return date timestamp.
    """
    books = load_data(BOOKS_FILE)
    records = load_data(BORROW_FILE)
    
    target_record = None
    for r in records:
        if (r['member_id'].strip().lower() == member_id.strip().lower() and 
            r['book_id'].strip().lower() == book_id.strip().lower() and 
            r['return_date'] is None):
            target_record = r
            break
            
    if not target_record:
        return False, "Transaction Error: No active matching borrow record found for this user and book combo."
        
    # Restore book inventory status
    for b in books:
        if b['book_id'].strip().lower() == book_id.strip().lower():
            b['available'] = min(b['quantity'], b['available'] + 1)
            break
            
    # Mark closing transaction stamp
    target_record['return_date'] = datetime.now().strftime("%Y-%m-%d")
    
    save_data(BOOKS_FILE, books)
    save_data(BORROW_FILE, records)
    return True, f"Success: Book ID '{book_id}' successfully returned by Member ID '{member_id}'."

def check_overdue_books():
    """
    Scans record lists and aggregates transactions that are unresolved past their assigned due date.
    """
    records = load_data(BORROW_FILE)
    overdue = []
    current_date = datetime.now().date()
    
    for r in records:
        if r['return_date'] is None:
            due = datetime.strptime(r['due_date'], "%Y-%m-%d").date()
            if current_date > due:
                overdue.append(r)
                
    return overdue