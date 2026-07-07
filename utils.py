# ==========================================
# Utility Module
# utils.py
# ==========================================


# ------------------------------------------
# Print Title
# ------------------------------------------

def print_title(title):

    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


# ------------------------------------------
# Success Message
# ------------------------------------------

def success(message):

    print(f"\n✅ {message}")


# ------------------------------------------
# Error Message
# ------------------------------------------

def error(message):

    print(f"\n❌ {message}")


# ------------------------------------------
# Confirmation Prompt
# ------------------------------------------

def confirm(message):

    choice = input(f"{message} (Y/N): ")

    return choice.lower() == "y"


# ------------------------------------------
# Input Validation
# ------------------------------------------

def not_empty(prompt):

    while True:

        value = input(prompt)

        if value.strip() == "":
            print("Input cannot be empty.")

        else:
            return value


# ------------------------------------------
# Integer Validation
# ------------------------------------------

def get_integer(prompt):

    while True:

        try:

            value = int(input(prompt))

            return value

        except ValueError:

            print("Please enter a valid integer.")