# ==========================================
# User Management Module
# ==========================================
from utils import print_title, success, error, not_empty, confirm
from file_handler import load_data, save_data
from auth import hash_password

USERS_FILE = "users.json"


# ------------------------------------------
# View All Users
# ------------------------------------------

def view_users():
    """Display all registered users (Admin only)"""
    
    users = load_data(USERS_FILE)
    
    print_title("ALL USERS")
    
    if len(users) == 0:
        print("No users registered.")
        return
    
    for user in users:
        print("-" * 40)
        print("Username :", user["username"])
        print("Role     :", user["role"])
    
    print("-" * 40)


# ------------------------------------------
# Search User
# ------------------------------------------

def search_user():
    """Search for a specific user by username"""
    
    users = load_data(USERS_FILE)
    
    print_title("SEARCH USER")
    
    username = not_empty("Enter Username to search: ")
    
    for user in users:
        if user["username"] == username:
            print("\n✓ User Found")
            print("-" * 40)
            print("Username :", user["username"])
            print("Role     :", user["role"])
            print("-" * 40)
            return
    
    error("User Not Found!")


# ------------------------------------------
# Change Password
# ------------------------------------------

def change_password(username):
    """Allow user to change their password"""
    
    users = load_data(USERS_FILE)
    
    print_title("CHANGE PASSWORD")
    
    user_found = False
    
    for user in users:
        if user["username"] == username:
            user_found = True
            
            old_password = input("Enter Old Password: ")
            
            # Verify old password
            if user["password"] != hash_password(old_password):
                error("Old password is incorrect!")
                return
            
            # Get new password
            new_password = not_empty("Enter New Password: ")
            confirm_password = not_empty("Confirm New Password: ")
            
            if new_password != confirm_password:
                error("Passwords do not match!")
                return
            
            # Update password
            user["password"] = hash_password(new_password)
            save_data(USERS_FILE, users)
            success("Password changed successfully!")
            return
    
    if not user_found:
        error("User not found!")


# ------------------------------------------
# Delete User
# ------------------------------------------

def delete_user():
    """Delete a user (Admin only)"""
    
    users = load_data(USERS_FILE)
    
    print_title("DELETE USER")
    
    username = not_empty("Enter Username to delete: ")
    
    user_index = -1
    
    for i, user in enumerate(users):
        if user["username"] == username:
            user_index = i
            break
    
    if user_index == -1:
        error("User not found!")
        return
    
    # Confirm deletion
    if not confirm(f"Are you sure you want to delete user '{username}'?"):
        print("Deletion cancelled.")
        return
    
    deleted_user = users.pop(user_index)
    save_data(USERS_FILE, users)
    success(f"User '{username}' deleted successfully!")


# ------------------------------------------
# Update User Role
# ------------------------------------------

def update_user_role():
    """Update a user's role (Admin only)"""
    
    users = load_data(USERS_FILE)
    
    print_title("UPDATE USER ROLE")
    
    username = not_empty("Enter Username: ")
    
    user_found = False
    
    for user in users:
        if user["username"] == username:
            user_found = True
            
            print(f"\nCurrent Role: {user['role']}")
            print("Select New Role:\n1. Admin\n2. Member")
            
            role_choice = input("Enter choice [1-2]: ")
            
            if role_choice == "1":
                user["role"] = "Admin"
            elif role_choice == "2":
                user["role"] = "Member"
            else:
                error("Invalid choice!")
                return
            
            save_data(USERS_FILE, users)
            success(f"Role updated to '{user['role']}' for user '{username}'!")
            return
    
    if not user_found:
        error("User not found!")


# ------------------------------------------
# User Management Menu
# ------------------------------------------

def user_menu():
    """User management menu (Admin only)"""
    
    while True:
        print("\n" + "=" * 60)
        print("              USER MANAGEMENT")
        print("=" * 60)
        
        print("1. View All Users")
        print("2. Search User")
        print("3. Update User Role")
        print("4. Delete User")
        print("5. Back to Admin Dashboard")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            view_users()
        
        elif choice == "2":
            search_user()
        
        elif choice == "3":
            update_user_role()
        
        elif choice == "4":
            delete_user()
        
        elif choice == "5":
            break
        
        else:
            error("Invalid choice!")
