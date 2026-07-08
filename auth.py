# ==========================================
# Authentication Module
# ==========================================
from utils import success, error, not_empty, is_valid_email, is_valid_phone, confirm
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
    
    # Choose role
    print("Select Role:\n1. Admin\n2. Member")
    role_choice = input("Enter choice [1-2] (default 1): ")

    if role_choice.strip() == "2":
        role = "Member"
    else:
        role = "Admin"

    # Check duplicate username
    for user in users:
        if user["username"] == username:
            print("Username already exists!")
            return

    hashed_password = hash_password(password)

    new_user = {
        "username": username,
        "password": hashed_password,
        "role": role
    }

    # If registering a Member, create a member record and link it
    if role == "Member":

        MEMBERS_FILE = "members.json"

        members = load_data(MEMBERS_FILE)

        while True:

            member_id = not_empty("Enter Member ID: ")

            # Check duplicate member_id
            duplicate = False

            for m in members:
                if m.get("member_id") == member_id:
                    duplicate = True
                    break

            if duplicate:
                print("Member ID already exists. Choose another.")
            else:
                break

        name = not_empty("Enter Member Name: ")

        while True:
            email = not_empty("Enter Email: ")
            if not is_valid_email(email):
                print("Enter a valid email address.")
            else:
                break

        while True:
            phone = not_empty("Enter Phone Number: ")
            if not is_valid_phone(phone):
                print("Enter a valid phone number (digits, +, -, spaces).")
            else:
                break

        new_member = {
            "member_id": member_id,
            "name": name,
            "email": email,
            "phone": phone
        }

        members.append(new_member)

        save_data(MEMBERS_FILE, members)

        print("\nMember profile created and linked to your account.")

        new_user["member_id"] = member_id

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