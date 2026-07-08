# ==========================================
# Member Management Module
# ==========================================
from utils import print_title, success, error, not_empty, is_valid_email, is_valid_phone, confirm
from file_handler import load_data, save_data

MEMBERS_FILE = "members.json"


# ------------------------------------------
# Register Member
# ------------------------------------------

def add_member():

    members = load_data(MEMBERS_FILE)

    print_title("REGISTER MEMBER")

    member_id = input("Enter Member ID: ")

    # Duplicate Member ID Check
    for member in members:
        if member["member_id"] == member_id:
            print("Member ID already exists!")
            return

    name = not_empty("Enter Member Name: ")

    # Validate email
    while True:
        email = not_empty("Enter Email: ")

        if not is_valid_email(email):
            print("Enter a valid email address.")
        else:
            break

    # Validate phone
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

    success("Member Registered Successfully!")


# ------------------------------------------
# View All Members
# ------------------------------------------

def view_members():

    members = load_data(MEMBERS_FILE)

    print("\n===== ALL MEMBERS =====")

    if len(members) == 0:
        print("No Members Found.")
        return

    for member in members:

        print("-" * 40)

        print("Member ID :", member["member_id"])
        print("Name      :", member["name"])
        print("Email     :", member["email"])
        print("Phone     :", member["phone"])

    print("-" * 40)


# ------------------------------------------
# Search Member
# ------------------------------------------

def search_member():

    members = load_data(MEMBERS_FILE)

    print("\n===== SEARCH MEMBER =====")

    member_id = input("Enter Member ID: ")

    for member in members:

        if member["member_id"] == member_id:

            print("\nMember Found")

            print("Member ID :", member["member_id"])
            print("Name      :", member["name"])
            print("Email     :", member["email"])
            print("Phone     :", member["phone"])

            return

    print("Member Not Found!")

    # ------------------------------------------
# Update Member
# ------------------------------------------

def update_member():

    members = load_data(MEMBERS_FILE)

    print("\n===== UPDATE MEMBER =====")

    member_id = input("Enter Member ID to Update: ")

    for member in members:

        if member["member_id"] == member_id:

            member["name"] = input("Enter New Name: ")
            member["email"] = input("Enter New Email: ")
            member["phone"] = input("Enter New Phone Number: ")

            save_data(MEMBERS_FILE, members)

            print("\nMember Updated Successfully!")

            return

    print("Member Not Found!")


# ------------------------------------------
# Delete Member
# ------------------------------------------

def delete_member():

    members = load_data(MEMBERS_FILE)

    print("\n===== DELETE MEMBER =====")

    member_id = input("Enter Member ID to Delete: ")

    for member in members:

        if member["member_id"] == member_id:

            if not confirm("Are you sure you want to delete this member?"):
                print("Deletion cancelled.")
                return

            members.remove(member)

            save_data(MEMBERS_FILE, members)

            print("\nMember Deleted Successfully!")

            return

    error("Member Not Found!")


# ------------------------------------------
# Member Management Menu
# ------------------------------------------

def member_menu():
    try:
        while True:

            print("\n" + "=" * 60)
            print("             MEMBER MANAGEMENT")
            print("=" * 60)

            print("1. Register Member")
            print("2. View Members")
            print("3. Search Member")
            print("4. Update Member")
            print("5. Delete Member")
            print("6. Back")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                add_member()

            elif choice == "2":
                view_members()

            elif choice == "3":
                search_member()

            elif choice == "4":
                update_member()

            elif choice == "5":
                delete_member()

            elif choice == "6":
                print("\nReturning to Admin Dashboard...")
                break

            else:
                print("Invalid Choice!")

    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted. Returning to Admin Dashboard...")
        return