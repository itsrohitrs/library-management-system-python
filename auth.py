import hashlib
from file_handler import load_data, save_data

USER_FILE = "users.json"

# This variable tracks the currently logged-in user session
# Structure when logged in: {"username": "admin", "role": "Librarian"}
current_session = None

def hash_password(password):
    """
    Converts a plain-text password into a secure SHA-256 hash string.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_librarian(username, password):
    """
    Registers a new Librarian account.
    Checks for duplicate usernames before saving.
    """
    if not username or not password:
        return False, "Username and password cannot be empty."
        
    users = load_data(USER_FILE)
    
    # Check if username already exists (Duplicate Check)
    for user in users:
        if user['username'].lower() == username.lower():
            return False, "Username already exists!"
            
    # Hash the password before saving for security
    hashed_password = hash_password(password)
    
    new_user = {
        "username": username,
        "password": hashed_password,
        "role": "Librarian"
    }
    
    users.append(new_user)
    save_data(USER_FILE, users)
    return True, f"Librarian '{username}' registered successfully."

def login(username, password):
    """
    Validates credentials and initializes the global session.
    """
    global current_session
    if not username or not password:
        return False, "Username and password cannot be empty."
        
    users = load_data(USER_FILE)
    hashed_input = hash_password(password)
    
    for user in users:
        if user['username'] == username and user['password'] == hashed_input:
            current_session = {
                "username": user['username'],
                "role": user['role']
            }
            return True, f"Welcome back, {user['username']}!"
            
    return False, "Invalid username or password."

def logout():
    """
    Clears the active session.
    """
    global current_session
    if current_session:
        username = current_session['username']
        current_session = None
        return True, f"User '{username}' logged out successfully."
    return False, "No active session to log out from."

def is_logged_in():
    """
    Helper function to check if a user is authenticated.
    """
    return current_session is not None