import json
import os

def load_data(filepath):
    """
    Safely reads data from a JSON file.
    If the file is missing or corrupted, handles the exception 
    and returns an empty list to keep the program running.
    """
    if not os.path.exists(filepath):
        # File doesn't exist yet; create it with an empty list
        save_data(filepath, [])
        return []
        
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"\n[!] Warning: {filepath} was corrupted. Initializing an empty database.")
        return []
    except Exception as e:
        print(f"\n[!] Unexpected error loading {filepath}: {e}")
        return []

def save_data(filepath, data):
    """
    Writes data into a JSON file with clean formatting (indentation).
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"\n[!] Error saving data to {filepath}: {e}")
        return False