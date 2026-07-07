from file_handler import load_data, save_data

MEMBERS_FILE = "members.json"

def register_member(member_id, name, email, phone):
    """
    Registers a new library member. Enforces unique Member ID check.
    """
    if not member_id or not name or not email or not phone:
        return False, "All fields are required."

    members = load_data(MEMBERS_FILE)
    
    # Check for Duplicate Member ID
    for member in members:
        if member['member_id'].strip().lower() == member_id.strip().lower():
            return False, f"Duplicate Error: Member ID '{member_id}' already exists."

    new_member = {
        "member_id": member_id.strip(),
        "name": name.strip(),
        "email": email.strip(),
        "phone": phone.strip()
    }
    
    members.append(new_member)
    save_data(MEMBERS_FILE, members)
    return True, f"Member '{name}' registered successfully."

def view_all_members():
    """
    Returns a list of all registered members.
    """
    return load_data(MEMBERS_FILE)

def search_members(query, search_by="name"):
    """
    Searches members by name or member_id using partial matching.
    """
    members = load_data(MEMBERS_FILE)
    results = []
    query = query.strip().lower()
    
    for member in members:
        if query in member.get(search_by, "").lower():
            results.append(member)
            
    return results

def update_member(member_id, name=None, email=None, phone=None):
    """
    Updates details for a specific member by their ID.
    """
    members = load_data(MEMBERS_FILE)
    found = False
    
    for member in members:
        if member['member_id'].strip().lower() == member_id.strip().lower():
            found = True
            if name: member['name'] = name.strip()
            if email: member['email'] = email.strip()
            if phone: member['phone'] = phone.strip()
            break
            
    if not found:
        return False, f"Member ID '{member_id}' not found."
        
    save_data(MEMBERS_FILE, members)
    return True, f"Member ID '{member_id}' successfully updated."

def delete_member(member_id):
    """
    Removes a member from the database.
    """
    members = load_data(MEMBERS_FILE)
    initial_count = len(members)
    
    members = [m for m in members if m['member_id'].strip().lower() != member_id.strip().lower()]
    
    if len(members) == initial_count:
        return False, f"Member ID '{member_id}' not found."
        
    save_data(MEMBERS_FILE, members)
    return True, f"Member ID '{member_id}' successfully removed from the system."