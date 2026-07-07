# ==========================================
# Authentication Module
# ==========================================
from utils import success, error, not_empty
import hashlib
from file_handler import load_data, save_data

USERS_FILE = "users.json"


# ------------------------------------------
# Hash Password
# ------------------------------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ------------------------------------------
# Register Librarian
# ------------------------------------------

def register():

    users = load_data(USERS_FILE)

    username = not_empty("Enter Username: ")
    password = not_empty("Enter Password: ")

    # Check duplicate username
    for user in users:
        if user["username"] == username:
            print("Username already exists!")
            return

    hashed_password = hash_password(password)

    new_user = {
        "username": username,
        "password": hashed_password,
        "role": "Admin"
    }

    users.append(new_user)

    save_data(USERS_FILE, users)

    success("Registration Successful!")


# ------------------------------------------
# Login
# ------------------------------------------

def login():

    users = load_data(USERS_FILE)

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    hashed_password = hash_password(password)

    for user in users:

        if user["username"] == username and user["password"] == hashed_password:

            success("Login Successful!")
            return user

    error("Invalid Username or Password!")

    return None