# ==========================================
# File Handler Module
# ==========================================

import json
import os


# Load data from a JSON file
def load_data(filename):

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data

    except json.JSONDecodeError:
        return []


# Save data to a JSON file
def save_data(filename, data):
    # Write atomically: write to a temp file then replace
    temp_filename = filename + ".tmp"

    with open(temp_filename, "w") as file:
        json.dump(data, file, indent=4)

    try:
        os.replace(temp_filename, filename)
    except Exception:
        # Fallback to simple write if atomic replace fails
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)